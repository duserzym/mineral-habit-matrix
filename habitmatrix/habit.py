"""Crystal forms -> polyhedra, and solvers that turn *relative face development*
(the quantity used in morphological typologies such as Pupin 1980) into face
central distances.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .lattice import Lattice, equivalent_normals, format_index, point_group, to_miller
from .polyhedron import Polyhedron, intersect_halfspaces, section_edge_fractions

ABSENT = None  # a form whose distance is None is not part of the habit


@dataclass(frozen=True)
class Form:
    key: str
    index: tuple  # (hkl) or (hkil) of one representative face
    name: str
    color: str

    @property
    def label(self) -> str:
        return "{" + format_index(self.index) + "}"


@dataclass
class Crystal:
    mineral: str
    lattice: Lattice
    point_group: str
    forms: list[Form]
    elongation_axis: tuple | None = (0, 0, 1)  # direct-lattice [uvw]
    # length is measured along this axis; (hkl) here means "normal to (hkl)" (e.g. mica
    # thickness normal to (001)); default = the elongation axis
    measure_plane: tuple | None = None
    _ops: list = field(init=False, repr=False)

    def __post_init__(self):
        self._ops = point_group(self.point_group)
        self._faces = {}
        for f in self.forms:
            n0 = self.lattice.face_normal(f.index)
            self._faces[f.key] = equivalent_normals(n0, self._ops)

    def form(self, key) -> Form:
        return next(f for f in self.forms if f.key == key)

    @property
    def axis(self) -> np.ndarray | None:
        return None if self.elongation_axis is None else self.lattice.axis(self.elongation_axis)

    @property
    def measure_axis(self) -> np.ndarray | None:
        if self.measure_plane is not None:
            return self.lattice.face_normal(self.measure_plane)
        return self.axis

    def planes(self, distances: dict, t: float = 0.0):
        """Yield (form, hkl, normal, distance).  `t` translates the two caps of the
        crystal rigidly along the elongation axis (prism faces are unaffected)."""
        u = self.axis
        for key, d in distances.items():
            if d is ABSENT:
                continue
            for n in self._faces[key]:
                shift = abs(float(n @ u)) * t if u is not None else 0.0
                yield key, self.lattice.miller_of(n), n, d + shift

    def solid(self, distances: dict, t: float = 0.0) -> Polyhedron:
        return intersect_halfspaces(self.planes(distances, t))

    # -- relative development ----------------------------------------------
    def prism_fractions(self, distances: dict) -> dict[str, float]:
        """Perimeter fraction of each prism form in the section normal to the axis."""
        u = self.axis
        e1 = np.cross(u, [1.0, 0, 0] if abs(u[0]) < 0.9 else [0, 1.0, 0])
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(u, e1)
        N, D, L = [], [], []
        for key, d in distances.items():
            if d is ABSENT:
                continue
            for n in self._faces[key]:
                if abs(n @ u) < 1e-9:
                    N.append([n @ e1, n @ e2])
                    D.append(d)
                    L.append(key)
        return section_edge_fractions(N, D, L)

    def area_fractions(self, distances: dict, keys, t: float = 0.0) -> dict[str, float]:
        areas = self.solid(distances, t).form_areas()
        tot = sum(areas.get(k, 0.0) for k in keys)
        return {k: areas.get(k, 0.0) / tot for k in keys}


def _bisect(fun, target, lo, hi, iters=60):
    """Solve fun(x) = target for x in [lo, hi], fun monotonic (either sense), in log x."""
    flo, fhi = fun(lo), fun(hi)
    if (flo - target) * (fhi - target) > 0:
        raise ValueError(f"target {target} not bracketed: f({lo})={flo}, f({hi})={fhi}")
    a, b = np.log(lo), np.log(hi)
    for _ in range(iters):
        m = 0.5 * (a + b)
        fm = fun(np.exp(m))
        if (fm - target) * (flo - target) <= 0:
            b = m
        else:
            a, flo = m, fm
    return float(np.exp(0.5 * (a + b)))


def solve_pair(crystal: Crystal, distances: dict, keep: str, vary: str, frac_keep: float,
               mode: str = "area", t: float = 50.0, lo: float = 0.05, hi: float = 20.0) -> dict:
    """Set the distance of `vary` (relative to `keep`) so that form `keep` makes up
    `frac_keep` of the pair's development.  frac_keep = 1 removes `vary`;
    frac_keep = 0 removes `keep`.

    mode = "prism": fraction of the cross-section perimeter (faces parallel to the axis)
    mode = "area":  fraction of face area (caps measured on a long crystal, t >> 1)
    """
    d = dict(distances)
    if frac_keep >= 1.0:
        d[vary] = ABSENT
        return d
    if frac_keep <= 0.0:
        # keep only `vary`: put it where it would be at a tiny fraction of `keep`
        d = solve_pair(crystal, distances, keep, vary, 1e-3, mode, t, lo, hi)
        d[keep] = ABSENT
        return d
    base = d[keep]

    def frac(x):
        d[vary] = base * x
        try:
            if mode == "prism":
                return crystal.prism_fractions(d).get(keep, 0.0)
            return crystal.area_fractions(d, [keep, vary], t)[keep]
        except Exception:
            return np.nan

    # scan for a bracket (fraction rises with x as `vary` retreats)
    xs = np.geomspace(lo, hi, 80)
    fs = np.array([frac(x) for x in xs])
    ok = ~np.isnan(fs)
    xs, fs = xs[ok], fs[ok]
    above = np.where(fs >= frac_keep)[0]
    below = np.where(fs < frac_keep)[0]
    if len(above) == 0 or len(below) == 0:
        raise ValueError(f"{crystal.mineral}: cannot reach {keep} fraction {frac_keep}")
    i = above[0]
    x = _bisect(frac, frac_keep, xs[i - 1], xs[i]) if i > 0 else xs[0]
    d[vary] = base * x
    return d


def solve_share(crystal: Crystal, distances: dict, key: str, share: float, ref_key: str,
                among: list[str] | None = None, t: float = 50.0, lo: float = 0.05, hi: float = 20.0) -> dict:
    """Set the distance of `key` (relative to form `ref_key`) so that it makes up `share`
    of the area of the forms in `among` (default: all forms present)."""
    d = dict(distances)
    if share <= 0.0:
        d[key] = ABSENT
        return d
    base = d[ref_key]

    def frac(x):
        d[key] = base * x
        try:
            areas = crystal.solid(d, t).form_areas()
        except Exception:
            return np.nan
        keys = among or list(areas)
        return areas.get(key, 0.0) / sum(areas.get(k, 0.0) for k in keys)

    xs = np.geomspace(lo, hi, 80)
    fs = np.array([frac(x) for x in xs])
    ok = ~np.isnan(fs)
    xs, fs = xs[ok], fs[ok]
    below = np.where(fs <= share)[0]  # share falls as `key` retreats
    if len(below) == 0 or below[0] == 0:
        raise ValueError(f"{crystal.mineral}: cannot reach {key} share {share}")
    i = below[0]
    d[key] = base * _bisect(frac, share, xs[i - 1], xs[i])
    return d


def solve_aspect(crystal: Crystal, distances: dict, aspect: float, t_hi: float = 200.0) -> float:
    """Cap translation t giving (length along axis) / (max width normal to it) = aspect."""
    u = crystal.measure_axis
    e1 = np.cross(u, [1.0, 0, 0] if abs(u[0]) < 0.9 else [0, 1.0, 0])
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(u, e1)
    dirs = [np.cos(a) * e1 + np.sin(a) * e2 for a in np.linspace(0, np.pi, 72, endpoint=False)]

    def ratio(t):
        p = crystal.solid(distances, t)
        return p.extent(u) / max(p.extent(v) for v in dirs)

    if ratio(0.0) >= aspect:
        return 0.0
    return _bisect(ratio, aspect, 1e-4, t_hi)
