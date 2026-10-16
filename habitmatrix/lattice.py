"""Lattices, reciprocal lattices, Miller indices and point-group symmetry.

Cartesian frame convention (used everywhere in this package):
    c  is parallel to +z,
    b  lies in the yz-plane,
    a  completes the right-handed set.
For monoclinic (b-unique) cells this puts b along y and the 2-fold axis along y;
for tetragonal, hexagonal and cubic cells it puts c along z.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True)
class Lattice:
    a: float
    b: float
    c: float
    alpha: float = 90.0
    beta: float = 90.0
    gamma: float = 90.0
    _basis: np.ndarray = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        al, be, ga = np.radians([self.alpha, self.beta, self.gamma])
        cvec = np.array([0.0, 0.0, self.c])
        bvec = np.array([0.0, self.b * np.sin(al), self.b * np.cos(al)])
        az = self.a * np.cos(be)
        ay = self.a * (np.cos(ga) - np.cos(al) * np.cos(be)) / np.sin(al)
        ax = np.sqrt(self.a**2 - ay**2 - az**2)
        avec = np.array([ax, ay, az])
        object.__setattr__(self, "_basis", np.vstack([avec, bvec, cvec]))

    @property
    def direct(self) -> np.ndarray:
        """Rows are the direct lattice vectors a, b, c (Cartesian, Å)."""
        return self._basis

    @property
    def reciprocal(self) -> np.ndarray:
        """Rows are a*, b*, c* (no 2π factor)."""
        a, b, c = self._basis
        vol = np.dot(a, np.cross(b, c))
        return np.vstack([np.cross(b, c), np.cross(c, a), np.cross(a, b)]) / vol

    def face_normal(self, hkl) -> np.ndarray:
        """Unit outward normal of the (hkl) plane: h a* + k b* + l c*."""
        n = np.asarray(to_miller(hkl), float) @ self.reciprocal
        return n / np.linalg.norm(n)

    def axis(self, uvw) -> np.ndarray:
        """Unit vector along the direct-lattice direction [uvw]."""
        v = np.asarray(uvw, float) @ self.direct
        return v / np.linalg.norm(v)

    def miller_of(self, normal) -> tuple[int, ...]:
        """Smallest integer (hkl) whose plane normal is parallel to `normal`."""
        v = self.direct @ np.asarray(normal, float)  # h = n·a, k = n·b, l = n·c
        v = v / np.abs(v[np.abs(v) > 1e-9]).min()
        for mult in range(1, 13):
            w = v * mult
            if np.allclose(w, np.round(w), atol=1e-4):
                w = np.round(w).astype(int)
                g = np.gcd.reduce(np.abs(w[w != 0]))
                return tuple(int(x) for x in w // g)
        raise ValueError(f"no small Miller index for {normal}")

    def to_dict(self) -> dict:
        return dict(a=self.a, b=self.b, c=self.c, alpha=self.alpha, beta=self.beta, gamma=self.gamma)


def to_miller(idx) -> tuple[int, int, int]:
    """Accept (hkl) or Miller–Bravais (hkil); return (hkl)."""
    idx = tuple(idx)
    if len(idx) == 4:
        h, k, i, l = idx
        if h + k + i != 0:
            raise ValueError(f"invalid Miller–Bravais index {idx}: h+k+i must be 0")
        return (h, k, l)
    return idx


def format_index(idx) -> str:
    """Crystallographic notation with overbars, e.g. (1,0,-1,1) -> '10̅1̅1'."""
    return "".join(f"{abs(x)}̅" if x < 0 else str(x) for x in idx)


# ---------------------------------------------------------------------------
# Point groups as Cartesian orthogonal matrices in the frame defined above.

def _rot(axis, deg):
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    t = np.radians(deg)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K


def _mirror(normal):
    n = np.asarray(normal, float) / np.linalg.norm(normal)
    return np.eye(3) - 2 * np.outer(n, n)


_A1 = [3**0.5 / 2, -0.5, 0]  # hexagonal a1 in this frame (c along z, b along y)
_I = -np.eye(3)
_X, _Y, _Z, _XY, _111 = [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 1, 1]

# Generators of the 32 crystallographic point groups in the Cartesian frame above.
# Monoclinic: b-unique (2-fold along y).  Tetragonal/hexagonal/trigonal: main axis along z.
# Trigonal and hexagonal secondary elements follow the "...m1 / ...21" convention: 2-fold
# axes along, and mirror normals parallel to, the a axes.
_GENERATORS = {
    "1": [],
    "-1": [_I],
    "2": [_rot(_Y, 180)],
    "m": [_mirror(_Y)],
    "2/m": [_rot(_Y, 180), _I],
    "222": [_rot(_Z, 180), _rot(_Y, 180)],
    "mm2": [_rot(_Z, 180), _mirror(_X)],
    "mmm": [_rot(_Z, 180), _rot(_Y, 180), _I],
    "4": [_rot(_Z, 90)],
    "-4": [_I @ _rot(_Z, 90)],
    "4/m": [_rot(_Z, 90), _I],
    "422": [_rot(_Z, 90), _rot(_X, 180)],
    "4mm": [_rot(_Z, 90), _mirror(_X)],
    "-42m": [_I @ _rot(_Z, 90), _rot(_X, 180)],
    "4/mmm": [_rot(_Z, 90), _mirror(_X), _I],
    "3": [_rot(_Z, 120)],
    "-3": [_rot(_Z, 120), _I],
    "32": [_rot(_Z, 120), _rot(_A1, 180)],
    "3m": [_rot(_Z, 120), _mirror(_A1)],
    "-3m": [_rot(_Z, 120), _mirror(_A1), _I],
    "6": [_rot(_Z, 60)],
    "-6": [_I @ _rot(_Z, 60)],
    "6/m": [_rot(_Z, 60), _I],
    "622": [_rot(_Z, 60), _rot(_A1, 180)],
    "6mm": [_rot(_Z, 60), _mirror(_A1)],
    "-6m2": [_I @ _rot(_Z, 60), _mirror(_A1)],
    "6/mmm": [_rot(_Z, 60), _mirror(_A1), _I],
    "23": [_rot(_Z, 180), _rot(_111, 120)],
    "m-3": [_rot(_Z, 180), _rot(_111, 120), _I],
    "432": [_rot(_Z, 90), _rot(_111, 120)],
    "-43m": [_I @ _rot(_Z, 90), _rot(_111, 120)],
    "m-3m": [_rot(_Z, 90), _rot(_111, 120), _I],
}


def point_group(symbol: str) -> list[np.ndarray]:
    """All operations of a crystallographic point group (closure of its generators)."""
    ops = [np.eye(3)]
    frontier = list(ops)
    gens = _GENERATORS[symbol]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                m = np.round(h @ g, 12)
                if not any(np.allclose(m, o, atol=1e-9) for o in ops):
                    ops.append(m)
                    new.append(m)
        frontier = new
    return ops


def equivalent_normals(normal, ops) -> list[np.ndarray]:
    out: list[np.ndarray] = []
    for op in ops:
        v = op @ normal
        if not any(np.allclose(v, w, atol=1e-8) for w in out):
            out.append(v)
    return out
