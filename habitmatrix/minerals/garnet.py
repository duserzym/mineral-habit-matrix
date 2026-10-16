"""Garnet: rhombic dodecahedron {110} <-> trapezohedron {211}, with a hexoctahedron {321} modifier.

Rows   : {211} share of the {110}+{211} area.
Columns: {321} share of the total area.
"""

from ..habit import ABSENT, Crystal, Form, solve_pair, solve_share
from ..lattice import Lattice
from ._common import ref, frac_text

ID = "garnet"
ROWS = [0.0, 0.25, 0.5, 0.75, 1.0]  # {211} share of {110}+{211}
COLS = [0.0, 0.1, 0.25]             # {321} share of total area


def crystal() -> Crystal:
    return Crystal(
        "garnet",
        Lattice(11.526, 11.526, 11.526),
        "m-3m",
        [
            Form("110", (1, 1, 0), "rhombic dodecahedron d", "#8e2a35"),
            Form("211", (2, 1, 1), "trapezohedron n", "#c46a4c"),
            Form("321", (3, 2, 1), "hexoctahedron s", "#d6b25e"),
        ],
        elongation_axis=None,
    )


def spec() -> dict:
    gt = crystal()
    cells = []
    for i, f211 in enumerate(ROWS):
        d0 = solve_pair(gt, {"110": 1.0, "211": 1.0, "321": ABSENT}, "211", "110", f211)
        for j, f321 in enumerate(COLS):
            ref_key = "110" if d0.get("110") is not None else "211"
            d = solve_share(gt, {**d0, "321": d0[ref_key]}, "321", f321, ref_key) if f321 > 0 else dict(d0)
            cells.append({
                "id": f"G{i + 1}{'abc'[j]}", "row": i, "col": j, "label": f"G{i + 1}{'abc'[j]}",
                "description": f"{frac_text('{211}', '{110}', f211)}; {{321}} ≈ {round(100 * f321)}% of surface.",
                "default": (i, j) == (2, 0), "distances": d, "t": 0.0,
            })
    return {
        "id": ID, "name": "Garnet", "group": "Orthosilicates", "crystal": gt, "formula": "X₃Y₂(SiO₄)₃",
        "chronometers": "Sm–Nd, Lu–Hf, U–Pb, diffusion speedometry",
        "system": "Cubic", "setting": "Ia3̄d (almandine)",
        "lattice_source": "Handbook of Mineralogy (almandine); Novak &amp; Gibbs (1971)",
        "mono_color": "#9b3040",
        "view": {"tilt": 20, "turn": -28},
        "matrix": {
            "title": "Dodecahedron ↔ trapezohedron",
            "subtitle": "Rows run from the rhombic dodecahedron {110} to the trapezohedron {211}. Columns add hexoctahedron {321} truncations.",
            "row_title": "{110} → {211}", "col_title": "{321} modifier",
            "rows": [{"label": f"G{i + 1}", "detail": frac_text("{211}", "{110}", f)} for i, f in enumerate(ROWS)],
            "cols": [{"label": "abc"[j], "detail": f"{{321}} {round(100 * f)}%"} for j, f in enumerate(COLS)],
            "note": "",
        },
        "about": ABOUT,
        "habits": HABITS,
        "references": REFERENCES,
        "cells": cells,
    }


ABOUT = """
<p>Garnet is the archetypal metamorphic petrochronometer (Sm–Nd, Lu–Hf, diffusion speedometry). Its two common
habits are the rhombic dodecahedron d{110} and the trapezohedron n{211}, often combined, with the hexoctahedron s{321}
bevelling the d–n edges. Habit is tied mostly to composition: Mn-rich, Ca-poor garnet tends towards {211}, Ca-rich
garnet towards {110}, and fast heating favours {211} (Sepahi 2007). Rough, stepped faces record diffusion-controlled
growth (Gulbin &amp; Glazov 2013). X-ray CT gives garnet size, shape and position in 3D for nucleation and growth
studies.</p>
"""

HABITS = [
    {"name": "Dodecahedron", "text": "d{110} only (row G1)."},
    {"name": "Trapezohedron", "text": "n{211} only (row G5)."},
    {"name": "d + n combinations", "text": "One form truncating the edges of the other (rows G2–G4)."},
    {"name": "d + n + s", "text": "The hexoctahedron s{321} bevels the d–n edges (columns b–c)."},
]

REFERENCES = [
    ref("Baxter, E.F., Caddick, M.J., Dragovic, B. (2017). Garnet: a rock-forming mineral petrochronometer. <i>Reviews in Mineralogy and Geochemistry</i> 83, 469–533.",
        "10.2138/rmg.2017.83.15", "Review of garnet petrochronology.", ["review"]),
    ref("Sepahi, A.A. (2007). A detailed study of morphology and chemistry of garnet crystals with suggestion of new subdivisions: data from pelitic schists, hornfelses and aplites of Hamedan region, Iran. <i>Iranian Journal of Science and Technology, Transaction A</i> 31(3), 281–289.",
        "10.22099/ijsts.2007.2345", "The closest thing to a garnet habit typology: {110} versus {211} tied to composition and heating rate. A regional study.", ["typology"]),
    ref("Gulbin, Yu.L., Glazov, A.I. (2013). Morphological evidence for diffusion-controlled growth of garnet from metapelites. <i>Geology of Ore Deposits</i> 55, 686–691.",
        "10.1134/S1075701513080059", "Rough, stepped {110} faces indicate high supersaturation.", ["morphology"]),
    ref("Denison, C., Carlson, W.D., Ketcham, R.A. (1997). Three-dimensional quantitative textural analysis of metamorphic rocks using high-resolution computed X-ray tomography: Part I. Methods and techniques. <i>Journal of Metamorphic Geology</i> 15, 29–44.",
        "10.1111/j.1525-1314.1997.00006.x", "3D CT of garnet porphyroblasts.", ["geometry"]),
    ref("Denison, C., Carlson, W.D. (1997). Three-dimensional quantitative textural analysis of metamorphic rocks using high-resolution computed X-ray tomography: Part II. Application to natural samples. <i>Journal of Metamorphic Geology</i> 15, 45–57.",
        "10.1111/j.1525-1314.1997.00007.x", "Garnet size, shape and spatial statistics used for growth kinetics.", ["geometry"]),
    ref("Ketcham, R.A., Carlson, W.D. (2001). Acquisition, optimization and interpretation of X-ray computed tomographic imagery: applications to the geosciences. <i>Computers &amp; Geosciences</i> 27, 381–400.",
        "10.1016/S0098-3004(00)00116-3", "CT methods for 3D grain geometry.", ["geometry"]),
    ref("Ketcham, R.A. (2005). Computational methods for quantitative analysis of three-dimensional features in geological specimens. <i>Geosphere</i> 1, 32–41.",
        "10.1130/GES00001.1", "Quantifying 3D grain shapes.", ["geometry"]),
    ref("Carlson, W.D. (1989). The significance of intergranular diffusion to the mechanisms and kinetics of porphyroblast crystallization. <i>Contributions to Mineralogy and Petrology</i> 103, 1–24.",
        "10.1007/BF00371361", "Porphyroblast growth kinetics.", ["kinetics"]),
    ref("Ague, J.J., Carlson, W.D. (2013). Metamorphism as garnet sees it: the kinetics of nucleation and growth, equilibration, and diffusional relaxation. <i>Elements</i> 9, 439–445.",
        "10.2113/gselements.9.6.439", "Overview of garnet kinetics.", ["review"]),
    ref("Novak, G.A., Gibbs, G.V. (1971). The crystal chemistry of the silicate garnets. <i>American Mineralogist</i> 56, 791–825.",
        None, "Garnet structure and cell parameters.", ["lattice"], url="http://www.minsocam.org/ammin/AM56/AM56_791.pdf"),
]
