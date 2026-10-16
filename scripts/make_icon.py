"""Draw the repository icon: a Pupin S13 zircon rendered from the generator's own geometry.

    python scripts/make_icon.py            # writes site/icon.svg (and docs/icon.svg copy for the README)
"""

from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from habitmatrix.minerals import zircon  # noqa: E402
from habitmatrix.minerals._common import prism_then_cap  # noqa: E402

# warm zircon palette per form (base colours before lighting)
PALETTE = {"100": "#eab25a", "110": "#c8683a", "101": "#f6d29a", "211": "#dc9356"}
TURN, TILT = np.radians(-28), np.radians(14)
LIGHT = np.array([-0.45, -0.8, 0.55])
LIGHT /= np.linalg.norm(LIGHT)


def hex2rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def rgb2hex(c):
    return "#" + "".join(f"{int(np.clip(x, 0, 255)):02x}" for x in c)


def main():
    zr = zircon.crystal()
    base = {"100": 1.0, "110": 1.0, "101": 1.2, "211": 1.2, "301": None}
    d, t = prism_then_cap(zr, base, ("100", "110", 0.5), ("101", "211", 0.5), 2.3)
    poly = zr.solid(d, t)

    rz = np.array([[np.cos(TURN), -np.sin(TURN), 0], [np.sin(TURN), np.cos(TURN), 0], [0, 0, 1]])
    rx = np.array([[1, 0, 0], [0, np.cos(TILT), -np.sin(TILT)], [0, np.sin(TILT), np.cos(TILT)]])
    R = rx @ rz  # viewer looks along +y; screen x = x, screen up = z
    V = poly.vertices @ R.T
    xy = np.c_[V[:, 0], -V[:, 2]]
    lo, hi = xy.min(0), xy.max(0)
    size = 330.0 / (hi - lo).max()
    centre = np.array([256.0, 252.0])
    P = (xy - (lo + hi) / 2) * size + centre

    faces = []
    for f in poly.faces:
        n = R @ f.normal
        if n[1] >= -1e-9:  # back-facing
            continue
        shade = 0.66 + 0.48 * max(0.0, float(n @ LIGHT))
        col = rgb2hex(hex2rgb(PALETTE[f.form]) * shade + 255 * 0.06)
        pts = " ".join(f"{P[i, 0]:.1f},{P[i, 1]:.1f}" for i in f.loop)
        faces.append((float((V[f.loop, 1]).mean()), pts, col))
    faces.sort(key=lambda x: -x[0])  # far faces first (only front faces are drawn, so order is cosmetic)

    hull = " ".join(f"{x:.1f},{y:.1f}" for x, y in _hull(P[[i for f in poly.faces for i in f.loop]]))
    polys = "\n    ".join(f'<polygon points="{p}" fill="{c}"/>' for _, p, c in faces)
    edges = "\n    ".join(f'<polygon points="{p}"/>' for _, p, _ in faces)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-labelledby="title desc">
  <title id="title">Mineral Habit Matrix icon</title>
  <desc id="desc">A Pupin S13 zircon crystal, {{100}} and {{110}} prisms with {{101}} and {{211}} pyramids, drawn from the generator's own geometry on a softly shaded tile.</desc>
  <defs>
    <linearGradient id="tile" x2="0.8" y2="1">
      <stop stop-color="#ffffff"/><stop offset="1" stop-color="#f3ede6"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.45" r="0.5">
      <stop stop-color="#ffd9a8" stop-opacity="0.55"/><stop offset="1" stop-color="#ffd9a8" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="10" stdDeviation="11" flood-color="#3b1d0c" flood-opacity="0.22"/>
    </filter>
  </defs>
  <rect x="36" y="36" width="440" height="440" rx="88" fill="url(#tile)"/>
  <rect x="36" y="36" width="440" height="440" rx="88" fill="none" stroke="#e7ded3" stroke-width="10"/>
  <circle cx="256" cy="246" r="190" fill="url(#glow)"/>
  <g filter="url(#shadow)">
    <polygon points="{hull}" fill="#c8683a"/>
    {polys}
  </g>
  <g fill="none" stroke="#5b2a12" stroke-opacity="0.55" stroke-width="3.2" stroke-linejoin="round">
    {edges}
  </g>
  <polygon points="{hull}" fill="none" stroke="#4a210d" stroke-width="5" stroke-linejoin="round" stroke-opacity="0.8"/>
</svg>
'''
    (ROOT / "site" / "icon.svg").write_text(svg)
    print("wrote site/icon.svg", len(faces), "visible faces")


def _hull(pts):
    pts = sorted(set(map(tuple, np.round(pts, 3))))
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])  # noqa: E731
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


if __name__ == "__main__":
    main()
