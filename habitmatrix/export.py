"""Writers: binary STL, STEP (AP214 B-rep with planar faces) and JSON for the web viewer."""

from __future__ import annotations

import struct
from pathlib import Path

import numpy as np

from .polyhedron import Polyhedron


def write_stl(poly: Polyhedron, path: Path, name: str = "crystal") -> None:
    V = poly.vertices
    tris = poly.triangles()
    header = f"mineral-habit-matrix {name}".encode()[:80].ljust(80, b" ")
    with open(path, "wb") as fh:
        fh.write(header)
        fh.write(struct.pack("<I", len(tris)))
        for i, j, k, fi in tris:
            n = poly.faces[fi].normal
            fh.write(struct.pack("<12fH", *n, *V[i], *V[j], *V[k], 0))


def _f(x: float) -> str:
    s = f"{x:.9f}".rstrip("0")
    return s + "0" if s.endswith(".") else s


def _vec(v) -> str:
    return "(" + ",".join(_f(float(x)) for x in v) + ")"


def write_step(poly: Polyhedron, path: Path, name: str = "crystal", description: str = "") -> None:
    """Exact planar B-rep (MANIFOLD_SOLID_BREP of ADVANCED_FACEs), units: millimetre."""
    lines: list[str] = []

    def add(entity: str) -> int:
        lines.append(entity)
        return len(lines)

    ref = lambda i: f"#{i}"  # noqa: E731
    name_q = name.replace("'", "")

    # product / context boilerplate
    app_ctx = add("APPLICATION_CONTEXT('core data for automotive mechanical design processes')")
    add(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,{ref(app_ctx)})")
    prod_ctx = add(f"PRODUCT_CONTEXT('',{ref(app_ctx)},'mechanical')")
    product = add(f"PRODUCT('{name_q}','{name_q}','{description[:200]}',({ref(prod_ctx)}))")
    add(f"PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,({ref(product)}))")
    pdf = add(f"PRODUCT_DEFINITION_FORMATION('','',{ref(product)})")
    pd_ctx = add(f"PRODUCT_DEFINITION_CONTEXT('part definition',{ref(app_ctx)},'design')")
    pdef = add(f"PRODUCT_DEFINITION('design','',{ref(pdf)},{ref(pd_ctx)})")
    pds = add(f"PRODUCT_DEFINITION_SHAPE('','',{ref(pdef)})")
    u_len = add("(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.))")
    u_ang = add("(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.))")
    u_sol = add("(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT())")
    unc = add(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-07),{ref(u_len)},'distance_accuracy_value','confusion accuracy')")
    geo_ctx = add(
        "(GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT(("
        f"{ref(unc)}))GLOBAL_UNIT_ASSIGNED_CONTEXT(({ref(u_len)},{ref(u_ang)},{ref(u_sol)}))"
        "REPRESENTATION_CONTEXT('Context #1','3D Context with UNIT and UNCERTAINTY'))"
    )

    # topology
    V = poly.vertices
    pt = [add(f"CARTESIAN_POINT('',{_vec(v)})") for v in V]
    vx = [add(f"VERTEX_POINT('',{ref(p)})") for p in pt]
    edges: dict[tuple[int, int], int] = {}

    def edge(i: int, j: int) -> tuple[int, bool]:
        key = (min(i, j), max(i, j))
        if key not in edges:
            a, b = key
            d = V[b] - V[a]
            L = float(np.linalg.norm(d))
            dirn = add(f"DIRECTION('',{_vec(d / L)})")
            vec = add(f"VECTOR('',{ref(dirn)},{_f(L)})")
            line = add(f"LINE('',{ref(pt[a])},{ref(vec)})")
            edges[key] = add(f"EDGE_CURVE('',{ref(vx[a])},{ref(vx[b])},{ref(line)},.T.)")
        return edges[key], i < j

    faces = []
    for f in poly.faces:
        oes = []
        for a, b in zip(f.loop, f.loop[1:] + f.loop[:1]):
            e, same = edge(a, b)
            oes.append(add(f"ORIENTED_EDGE('',*,*,{ref(e)},{'.T.' if same else '.F.'})"))
        loop = add(f"EDGE_LOOP('',({','.join(ref(o) for o in oes)}))")
        bound = add(f"FACE_OUTER_BOUND('',{ref(loop)},.T.)")
        origin = add(f"CARTESIAN_POINT('',{_vec(V[f.loop[0]])})")
        axis = add(f"DIRECTION('',{_vec(f.normal)})")
        rd = V[f.loop[1]] - V[f.loop[0]]
        refdir = add(f"DIRECTION('',{_vec(rd / np.linalg.norm(rd))})")
        place = add(f"AXIS2_PLACEMENT_3D('',{ref(origin)},{ref(axis)},{ref(refdir)})")
        plane = add(f"PLANE('',{ref(place)})")
        label = f"{f.form} ({''.join(str(x) for x in f.index)})"
        faces.append(add(f"ADVANCED_FACE('{label}',({ref(bound)}),{ref(plane)},.T.)"))

    shell = add(f"CLOSED_SHELL('',({','.join(ref(x) for x in faces)}))")
    brep = add(f"MANIFOLD_SOLID_BREP('{name_q}',{ref(shell)})")
    o = add("CARTESIAN_POINT('',(0.,0.,0.))")
    z = add("DIRECTION('',(0.,0.,1.))")
    x = add("DIRECTION('',(1.,0.,0.))")
    world = add(f"AXIS2_PLACEMENT_3D('',{ref(o)},{ref(z)},{ref(x)})")
    rep = add(f"ADVANCED_BREP_SHAPE_REPRESENTATION('{name_q}',({ref(world)},{ref(brep)}),{ref(geo_ctx)})")
    add(f"SHAPE_DEFINITION_REPRESENTATION({ref(pds)},{ref(rep)})")

    header = (
        "ISO-10303-21;\nHEADER;\n"
        f"FILE_DESCRIPTION(('{description[:200]}'),'2;1');\n"
        f"FILE_NAME('{Path(path).name}','2026-01-01T00:00:00',(''),(''),'mineral-habit-matrix','mineral-habit-matrix','');\n"
        "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n"
    )
    body = "".join(f"#{i}={e};\n" for i, e in enumerate(lines, start=1))
    Path(path).write_text(header + body + "ENDSEC;\nEND-ISO-10303-21;\n")


def poly_to_json(poly: Polyhedron, ndigits: int = 5) -> dict:
    return {
        "vertices": np.round(poly.vertices, ndigits).tolist(),
        "faces": [{"form": f.form, "hkl": list(f.index), "loop": f.loop} for f in poly.faces],
    }
