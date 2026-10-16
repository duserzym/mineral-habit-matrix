"""Build every habit matrix: STL + STEP models and the JSON consumed by the website.

    python -m habitmatrix.build            # all minerals
    python -m habitmatrix.build zircon     # one mineral
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import numpy as np

from .export import poly_to_json, write_step, write_stl
from .habit import Crystal
from .minerals import GROUP_ORDER, MINERALS

ROOT = Path(__file__).resolve().parents[1]
SITE_DATA = ROOT / "site" / "data"
MODELS = ROOT / "models"


def _perp_dirs(u, n=72):
    e1 = np.cross(u, [1.0, 0, 0] if abs(u[0]) < 0.9 else [0, 1.0, 0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(u, e1)
    return [np.cos(a) * e1 + np.sin(a) * e2 for a in np.linspace(0, np.pi, n, endpoint=False)]


def _sphere_dirs(n=400):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = np.pi * (1 + 5**0.5) * i
    return np.c_[np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)]


def metrics(poly, crystal: Crystal) -> dict:
    V, A = poly.volume(), poly.surface_area()
    if crystal.axis is not None:
        u = crystal.measure_axis
        aspect = poly.extent(u) / max(poly.extent(v) for v in _perp_dirs(u))
    else:
        ext = [poly.extent(v) for v in _sphere_dirs()]
        aspect = max(ext) / min(ext)
    return {
        "volume": round(V, 6),
        "surface_area": round(A, 5),
        "rsv": round(3 * V / A, 5),
        "sphericity": round(np.pi ** (1 / 3) * (6 * V) ** (2 / 3) / A, 5),
        "aspect": round(float(aspect), 4),
    }


def _cap_shift(crystal: Crystal, key: str) -> float:
    """|n·u| for a form: how far its faces move per unit cap translation (same for every face of a form)."""
    if crystal.axis is None:
        return 0.0
    return abs(float(crystal._faces[key][0] @ crystal.axis))


def build_mineral(spec: dict) -> dict:
    crystal: Crystal = spec["crystal"]
    mid = spec["id"]
    stl_dir, step_dir = MODELS / "stl" / mid, MODELS / "step" / mid
    for d in (stl_dir, step_dir):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)

    ids = [c["id"] for c in spec["cells"]]
    clash = {i for i in ids if sum(j.lower() == i.lower() for j in ids) > 1}
    if clash:  # file names must stay unique on case-insensitive file systems (macOS, Windows)
        raise ValueError(f"{mid}: cell ids differ only by case: {sorted(clash)}")

    cells_out = []
    for cell in spec["cells"]:
        t = cell.get("t", 0.0)
        poly = crystal.solid(cell["distances"], t)
        scale = poly.volume() ** (-1 / 3)
        poly = poly.scaled(scale)  # unit volume, size is not modelled
        areas = poly.form_areas()
        tot = sum(areas.values())
        fname = f"{mid}_{cell['id']}"
        desc = f"{spec['name']} habit {cell['label']} - mineral-habit-matrix"
        write_stl(poly, stl_dir / f"{fname}.stl", fname)
        write_step(poly, step_dir / f"{fname}.step", fname, desc)
        out = {k: v for k, v in cell.items() if k not in ("distances", "t")}
        out["params"] = {
            "face_distances": {k: (None if v is None else round(v, 6)) for k, v in cell["distances"].items()},
            "cap_translation": round(t, 6),
            "scale": round(scale, 8),
            # effective central distance of every face of each form, after cap translation and
            # unit-volume scaling: the web viewer rebuilds the crystal from these half-spaces
            "planes": {k: round(scale * (v + _cap_shift(crystal, k) * t), 8)
                       for k, v in cell["distances"].items() if v is not None},
        }
        out["fractions"] = {k: round(areas[k] / tot, 4) for k in [f.key for f in crystal.forms] if k in areas}
        out["metrics"] = metrics(poly, crystal)
        out["geometry"] = poly_to_json(poly)
        out["files"] = {"stl": f"models/stl/{mid}/{fname}.stl", "step": f"models/step/{mid}/{fname}.step"}
        cells_out.append(out)

    L = crystal.lattice
    data = {
        "id": mid,
        "name": spec["name"],
        "group": spec.get("group", ""),
        "formula": spec.get("formula", ""),
        "chronometers": spec.get("chronometers", ""),
        "system": spec["system"],
        "point_group": crystal.point_group,
        "setting": spec.get("setting", ""),
        "lattice": {k: round(v, 4) for k, v in L.to_dict().items()},
        "lattice_source": spec.get("lattice_source", ""),
        "elongation_axis": list(crystal.elongation_axis) if crystal.elongation_axis else None,
        "mono_color": spec.get("mono_color", "#c9a27a"),
        "view": spec.get("view", {}),
        "forms": [{"key": f.key, "label": f.label, "index": list(f.index), "name": f.name, "color": f.color,
                   "normals": [np.round(n, 7).tolist() for n in crystal._faces[f.key]],
                   "hkls": [list(L.miller_of(n)) for n in crystal._faces[f.key]]}
                  for f in crystal.forms],
        "basis": np.round(L.direct, 6).tolist(),
        "reciprocal": np.round(L.reciprocal, 8).tolist(),
        "axis": None if crystal.axis is None else np.round(crystal.axis, 7).tolist(),
        "measure_axis": None if crystal.measure_axis is None else np.round(crystal.measure_axis, 7).tolist(),
        "pg_order": len(crystal._ops),
        "matrix": spec["matrix"],
        "about": spec.get("about", ""),
        "habits": spec.get("habits", []),
        "references": spec.get("references", []),
        "cells": cells_out,
    }
    (SITE_DATA / f"{mid}.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    default = next((c for c in cells_out if c.get("default")), cells_out[len(cells_out) // 2])
    return {"id": mid, "name": spec["name"], "group": spec.get("group", ""), "file": f"{mid}.json",
            "ncells": len(cells_out), "formula": spec.get("formula", ""),
            "chronometers": spec.get("chronometers", ""), "system": spec["system"],
            "matrix_title": spec["matrix"]["title"],
            # a representative crystal for the atlas page
            "preview": {"id": default["id"], "geometry": default["geometry"],
                        "forms": [{"key": f["key"], "color": f["color"]} for f in data["forms"]],
                        "mono_color": data["mono_color"], "view": data["view"]}}


def _build_one(mod_name: str) -> dict:
    import importlib
    mod = importlib.import_module(f"habitmatrix.minerals.{mod_name}")
    return build_mineral(mod.spec())


def main(argv=None):
    from concurrent.futures import ProcessPoolExecutor

    argv = sys.argv[1:] if argv is None else argv
    SITE_DATA.mkdir(parents=True, exist_ok=True)
    index_path = SITE_DATA / "index.json"
    index = {m["id"]: m for m in json.loads(index_path.read_text())} if index_path.exists() else {}
    todo = [m for m in MINERALS if not argv or m.ID in argv]
    with ProcessPoolExecutor() as pool:
        for mod, entry in zip(todo, pool.map(_build_one, [m.__name__.rsplit(".", 1)[1] for m in todo])):
            index[entry["id"]] = entry
            print(f"{entry['id']:12s} {entry['ncells']:3d} habits")
    ids = [m.ID for m in MINERALS]
    rank = {g: i for i, g in enumerate(GROUP_ORDER)}
    ordered = sorted((index[i] for i in ids if i in index), key=lambda e: (rank.get(e["group"], 99), ids.index(e["id"])))
    previews = {e["id"]: e.pop("preview", None) for e in ordered}
    old = json.loads((SITE_DATA / "atlas.json").read_text()) if (SITE_DATA / "atlas.json").exists() else {}
    atlas = {i: previews[i] or old.get(i) for i in previews}
    index_path.write_text(json.dumps(ordered, ensure_ascii=False, indent=1))
    (SITE_DATA / "atlas.json").write_text(json.dumps(atlas, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
