"""Monazite-(Ce): tabular on a{100} x elongation along b.

Setting: P2₁/n (a = 6.7902, b = 7.0203, c = 6.4674 Å, β = 103.38°; HoM, structure Ni et al. 1995).
Crystals elongated along [010] show the zone a{100}, w{101}, x{1̄01} and are terminated by
m{110} and e{011} (Dana 1892).  The sign convention of the {±101} pair is uncertain in the
sources, so both are included with equal central distance.

Rows   : a{100} central distance relative to {±101} (equant -> strongly tabular on a).
Columns: aspect ratio along b (equant -> elongate).
"""

from ..habit import Crystal, Form, solve_aspect
from ..lattice import Lattice
from ._common import ref

ID = "monazite"
A_DIST = [1.0, 0.85, 0.7, 0.55]
ASPECTS = [None, 1.6, 2.5, 4.0]  # None = equant (no extra elongation)
ROW_TEXT = ["equant zone", "a{100} moderate", "tabular on a", "strongly tabular"]


def crystal() -> Crystal:
    return Crystal(
        "monazite",
        Lattice(6.7902, 7.0203, 6.4674, 90, 103.38, 90),
        "2/m",
        [
            Form("100", (1, 0, 0), "a, tabular face", "#c0762e"),
            Form("101", (1, 0, 1), "w", "#e2b15b"),
            Form("-101", (-1, 0, 1), "x", "#d79a5a"),
            Form("110", (1, 1, 0), "m, termination", "#7d5a8c"),
            Form("011", (0, 1, 1), "e, termination", "#5a7d8c"),
        ],
        elongation_axis=(0, 1, 0),
    )


def spec() -> dict:
    mz = crystal()
    cells = []
    for i, da in enumerate(A_DIST):
        for j, asp in enumerate(ASPECTS):
            d = {"100": da, "101": 1.0, "-101": 1.0, "110": 1.1, "011": 1.1}
            t = solve_aspect(mz, d, asp) if asp else 0.0
            cells.append({
                "id": f"A{i + 1}E{j + 1}", "row": i, "col": j, "label": f"A{i + 1}·E{j + 1}",
                "description": (f"{ROW_TEXT[i]} (a{{100}} at {da:g}× the {{±101}} distance); "
                                + ("equant along b." if asp is None else f"elongated {asp:g}:1 along b.")),
                "default": (i, j) == (2, 1), "distances": d, "t": t,
            })
    return {
        "id": ID, "name": "Monazite", "crystal": mz, "formula": "(Ce,La,Nd,Th)PO₄",
        "chronometers": "U–Th–Pb (EPMA, LA-ICP-MS, SIMS), (U–Th)/He",
        "system": "Monoclinic", "setting": "P2₁/n",
        "lattice_source": "Handbook of Mineralogy; Ni et al. (1995)",
        "mono_color": "#c98a3e",
        "view": {"tilt": 18, "turn": -40},
        "matrix": {
            "title": "Tabular on {100} × elongation along b",
            "subtitle": "Rows flatten the crystal on a{100}, its commonest habit. Columns elongate it along [010], with m{110} and e{011} terminations.",
            "row_title": "a{100} development", "col_title": "Elongation along b",
            "rows": [{"label": f"A{i + 1}", "detail": t} for i, t in enumerate(ROW_TEXT)],
            "cols": [{"label": f"E{j + 1}", "detail": "equant" if a is None else f"{a:g}:1"} for j, a in enumerate(ASPECTS)],
            "note": ("No habit typology exists for monazite, so this grid spans the habits Dana (1892) and the Handbook of "
                     "Mineralogy describe. The signs of the w/x {±101} and r/v {±111} pairs are uncertain in the old "
                     "literature, so both members of {±101} are used at the same distance and {±111} is left out. "
                     "Cruciform twins on {100} are not modelled."),
        },
        "about": """
<p>Monazite is the main REE-phosphate petrochronometer. Its common habit is tabular on a{100}. Crystals can also be
elongated along b, in the zone of a, c and the {±101} forms, and terminated by m{110} and e{011}. Some are prismatic on
v{111}, equant, or wedge-shaped. Old monoclinic morphology uses the acute β, so the h index changes sign when
converting to the modern P2₁/n cell. Metamorphic monazite is often anhedral, and growth kinetics control its shape
(Ayers et al. 1999).</p>""",
        "habits": [
            {"name": "Tabular on a{100}", "text": "The commonest habit (rows A3–A4)."},
            {"name": "Elongate along b", "text": "The zone a + {±101}, terminated by m{110} and e{011} (columns E3–E4)."},
            {"name": "Equant / wedge-shaped", "text": "Short crystals in all directions (cell A1·E1)."},
            {"name": "Not modelled", "text": "Prismatic habits on v{111}, whose sign convention is uncertain, and cruciform twins on {100}."},
        ],
        "references": [
            ref("Engi, M. (2017). Petrochronology based on REE-minerals: monazite, allanite, xenotime, apatite. <i>Reviews in Mineralogy and Geochemistry</i> 83, 365–418.",
                "10.2138/rmg.2017.83.12", "Review of monazite and xenotime petrochronology.", ["review"]),
            ref("Williams, M.L., Jercinovic, M.J., Hetherington, C.J. (2007). Microprobe monazite geochronology: understanding geologic processes by integrating composition and chronology. <i>Annual Review of Earth and Planetary Sciences</i> 35, 137–175.",
                "10.1146/annurev.earth.35.031306.140228", "In-situ monazite dating tied to textures and growth domains.", ["review"]),
            ref("Ayers, J.C., Miller, C., Gorisch, B., Milleman, J. (1999). Textural development of monazite during high-grade metamorphism: hydrothermal growth kinetics, with implications for U,Th-Pb geochronology. <i>American Mineralogist</i> 84, 1766–1780.",
                "10.2138/am-1999-11-1206", "Links monazite crystal shape and size to growth kinetics.", ["morphology"]),
            ref("Rasmussen, B., Muhling, J.R. (2007). Monazite begets monazite: evidence for dissolution of detrital monazite and reprecipitation of syntectonic monazite during low-grade regional metamorphism. <i>Contributions to Mineralogy and Petrology</i> 154, 675–689.",
                "10.1007/s00410-007-0216-6", "Habit and shape of low-grade syntectonic monazite.", ["morphology"]),
            ref("Overstreet, W.C. (1967). The geologic occurrence of monazite. <i>U.S. Geological Survey Professional Paper</i> 530.",
                "10.3133/pp530", "A classic compilation of monazite occurrence and habit.", ["morphology"]),
            ref("Boyce, J.W., Hodges, K.V., Olszewski, W.J., Jercinovic, M.J. (2005). He diffusion in monazite: implications for (U-Th)/He thermochronometry. <i>Geochemistry, Geophysics, Geosystems</i> 6, Q12004.",
                "10.1029/2005GC001058", "He diffusion, where grain geometry acts as the diffusion domain.", ["thermochronology"]),
            ref("Ni, Y., Hughes, J.M., Mariano, A.N. (1995). Crystal chemistry of the monazite and xenotime structures. <i>American Mineralogist</i> 80, 21–26.",
                "10.2138/am-1995-1-203", "Structure of monazite and xenotime.", ["lattice"]),
        ],
        "cells": cells,
    }
