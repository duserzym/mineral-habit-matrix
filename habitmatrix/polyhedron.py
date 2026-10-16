"""Convex crystal polyhedra as intersections of face half-spaces  n·x <= d."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.spatial import HalfspaceIntersection


@dataclass
class Face:
    form: str  # key of the crystal form this face belongs to
    index: tuple  # Miller index of this individual face
    normal: np.ndarray
    distance: float
    loop: list[int]  # vertex indices, counter-clockwise seen from outside

    def area(self, verts: np.ndarray) -> float:
        p = verts[self.loop]
        return 0.5 * float(np.dot(np.cross(p - p[0], np.roll(p, -1, axis=0) - p[0]).sum(axis=0), self.normal))


@dataclass
class Polyhedron:
    vertices: np.ndarray
    faces: list[Face]

    # -- metrics -----------------------------------------------------------
    def face_areas(self) -> np.ndarray:
        return np.array([f.area(self.vertices) for f in self.faces])

    def form_areas(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for f, a in zip(self.faces, self.face_areas()):
            out[f.form] = out.get(f.form, 0.0) + a
        return out

    def surface_area(self) -> float:
        return float(self.face_areas().sum())

    def volume(self) -> float:
        return float(sum(f.distance * a for f, a in zip(self.faces, self.face_areas())) / 3.0)

    def extent(self, direction) -> float:
        u = np.asarray(direction, float)
        proj = self.vertices @ (u / np.linalg.norm(u))
        return float(proj.max() - proj.min())

    def triangles(self) -> list[tuple[int, int, int, int]]:
        """Fan triangulation; returns (i, j, k, face_number)."""
        tris = []
        for fi, f in enumerate(self.faces):
            for j in range(1, len(f.loop) - 1):
                tris.append((f.loop[0], f.loop[j], f.loop[j + 1], fi))
        return tris

    # -- transforms ----------------------------------------------------------
    def scaled(self, s: float) -> "Polyhedron":
        faces = [Face(f.form, f.index, f.normal, f.distance * s, list(f.loop)) for f in self.faces]
        return Polyhedron(self.vertices * s, faces)

    def rotated(self, R: np.ndarray) -> "Polyhedron":
        faces = [Face(f.form, f.index, R @ f.normal, f.distance, list(f.loop)) for f in self.faces]
        return Polyhedron(self.vertices @ R.T, faces)


def intersect_halfspaces(planes, rel_tol: float = 1e-7) -> Polyhedron:
    """planes: iterable of (form, index, unit_normal, distance) with distance > 0.

    The origin must lie strictly inside; it does for every crystal here because
    all face distances are measured from the crystal centre.
    """
    planes = list(planes)
    N = np.array([p[2] for p in planes], float)
    D = np.array([p[3] for p in planes], float)
    hs = HalfspaceIntersection(np.hstack([N, -D[:, None]]), np.zeros(3))
    pts = hs.intersections
    scale = np.abs(pts).max()
    tol = rel_tol * scale

    # merge numerically coincident vertices (several planes can meet at one point)
    verts: list[np.ndarray] = []
    for p in pts:
        if not any(np.linalg.norm(p - q) < 1e3 * tol for q in verts):
            verts.append(p)
    V = np.array(verts)

    faces: list[Face] = []
    for (form, idx, n, d) in planes:
        on = np.where(np.abs(V @ n - d) < 1e3 * tol)[0]
        if len(on) < 3:
            continue
        P = V[on]
        ctr = P.mean(axis=0)
        u = P[0] - ctr
        u -= n * np.dot(u, n)
        u /= np.linalg.norm(u)
        w = np.cross(n, u)
        ang = np.arctan2((P - ctr) @ w, (P - ctr) @ u)
        loop = [int(i) for i in on[np.argsort(ang)]]  # CCW about +n
        f = Face(form, tuple(idx), np.asarray(n, float), float(d), loop)
        if f.area(V) > (1e-9 * scale**2):
            faces.append(f)

    # drop vertices not used by any surviving face and re-index
    used = sorted({i for f in faces for i in f.loop})
    remap = {old: new for new, old in enumerate(used)}
    for f in faces:
        f.loop = [remap[i] for i in f.loop]
    return Polyhedron(V[used], faces)


def section_edge_fractions(normals2d, distances, labels) -> dict[str, float]:
    """Perimeter fraction per label of the 2D polygon  n·x <= d  (prism cross-section)."""
    N = np.asarray(normals2d, float)
    D = np.asarray(distances, float)
    hs = HalfspaceIntersection(np.hstack([N, -D[:, None]]), np.zeros(2))
    P = hs.intersections
    tol = 1e-7 * np.abs(P).max()
    lengths: dict[str, float] = {}
    for n, d, lab in zip(N, D, labels):
        on = P[np.abs(P @ n - d) < 1e3 * tol]
        if len(on) < 2:
            continue
        t = on @ np.array([-n[1], n[0]])
        lengths[lab] = lengths.get(lab, 0.0) + float(t.max() - t.min())
    total = sum(lengths.values())
    return {k: v / total for k, v in lengths.items()}
