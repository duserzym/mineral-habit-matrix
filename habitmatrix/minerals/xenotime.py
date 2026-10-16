"""Xenotime-(Y): zircon-structured (I4₁/amd) dipyramids and prisms.

Forms (structural indices, as for zircon): prisms {100}, {110}; dipyramid {101}.
Old literature uses the zircon-type morphological cell (old p{111} = {101}).

Rows   : aspect ratio along c (equant dipyramid -> prismatic, "resembling zircon").
Columns: {110} share of the prism cross-section.
"""

from ..habit import Crystal, Form
from ..lattice import Lattice
from ._common import frac_text, prism_then_cap, ref

ID = "xenotime"
ASPECTS = [1.0, 1.5, 2.2, 3.2]
P110 = [0.0, 0.3, 0.5]


def crystal() -> Crystal:
    return Crystal(
        "xenotime",
        Lattice(6.895, 6.895, 6.030),
        "4/mmm",
        [
            Form("100", (1, 0, 0), "prism", "#c7a23a"),
            Form("110", (1, 1, 0), "prism", "#a65a3a"),
            Form("101", (1, 0, 1), "dipyramid", "#6a86a8"),
        ],
        elongation_axis=(0, 0, 1),
    )


def spec() -> dict:
    xt = crystal()
    cells = []
    for i, asp in enumerate(ASPECTS):
        for j, f110 in enumerate(P110):
            d, t = prism_then_cap(xt, {"100": 1.0, "110": 1.0, "101": 1.0}, ("100", "110", 1 - f110), None, asp)
            cells.append({
                "id": f"X{i + 1}{'abc'[j]}", "row": i, "col": j, "label": f"X{i + 1}{'abc'[j]}", "sub": f"{asp:g}:1",
                "description": f"Prism: {frac_text('{100}', '{110}', 1 - f110)}; aspect {asp:g}:1 with {{101}} dipyramid.",
                "default": (i, j) == (1, 0), "distances": d, "t": t,
            })
    return {
        "id": ID, "name": "Xenotime", "crystal": xt, "formula": "YPO₄",
        "chronometers": "U–Th–Pb, diagenetic/hydrothermal dating, monazite–xenotime thermometry",
        "system": "Tetragonal", "setting": "I4₁/amd (zircon structure)",
        "lattice_source": "Handbook of Mineralogy (mid-range)",
        "mono_color": "#c2a050",
        "matrix": {
            "title": "Dipyramid → prism",
            "subtitle": "The {101} dipyramid with a {100} prism. Columns add the second prism {110}.",
            "row_title": "Aspect ratio (L/W)", "col_title": "Prism",
            "rows": [{"label": f"X{i + 1}", "detail": f"{a:g}:1"} for i, a in enumerate(ASPECTS)],
            "cols": [{"label": "abc"[j], "detail": frac_text("{100}", "{110}", 1 - f)} for j, f in enumerate(P110)],
            "note": ("No habit typology exists for xenotime. Dana's additional forms ({001}, {201}, {111}, {331}, {311}) use "
                     "the old zircon-type cell and are not modelled. Epitaxial overgrowths on zircon are composite crystals "
                     "and are not modelled either."),
        },
        "about": """
<p>Xenotime has the zircon structure. Its crystals are prismatic {100} + {101}, "resembling zircon", or equant
dipyramids dominated by {101}. Diagenetic and hydrothermal xenotime commonly grows epitaxially on detrital zircon,
sharing its c-axis (Rasmussen 2005). That epitaxial growth is what makes xenotime useful for dating sedimentary and
low-grade rocks.</p>""",
        "habits": [
            {"name": "Equant dipyramid", "text": "{101} dominant with a short prism (row X1)."},
            {"name": "Prismatic", "text": "{100} + {101}, similar to the zircon P and D types (rows X3–X4)."},
            {"name": "Prism with {110}", "text": "A second prism truncating the {100} edges (columns b–c)."},
            {"name": "Epitaxial on zircon", "text": "Composite crystals that share the zircon c-axis (not modelled)."},
        ],
        "references": [
            ref("Hetherington, C.J., Jercinovic, M.J., Williams, M.L., Mahan, K. (2008). Understanding geologic processes with xenotime: composition, chronology, and a protocol for electron probe microanalysis. <i>Chemical Geology</i> 254, 133–147.",
                "10.1016/j.chemgeo.2008.05.020", "Xenotime petrochronology protocols.", ["review"]),
            ref("Rasmussen, B. (2005). Radiometric dating of sedimentary rocks: the application of diagenetic xenotime geochronology. <i>Earth-Science Reviews</i> 68, 197–243.",
                "10.1016/j.earscirev.2004.05.004", "Documents the habit of xenotime grown epitaxially on zircon.", ["morphology", "review"]),
            ref("Pyle, J.M. (2001). Monazite-xenotime-garnet equilibrium in metapelites and a new monazite-garnet thermometer. <i>Journal of Petrology</i> 42, 2083–2107.",
                "10.1093/petrology/42.11.2083", "Xenotime in metapelite phase equilibria.", ["petrology"]),
            ref("Engi, M. (2017). Petrochronology based on REE-minerals: monazite, allanite, xenotime, apatite. <i>Reviews in Mineralogy and Geochemistry</i> 83, 365–418.",
                "10.2138/rmg.2017.83.12", "Review.", ["review"]),
            ref("Ni, Y., Hughes, J.M., Mariano, A.N. (1995). Crystal chemistry of the monazite and xenotime structures. <i>American Mineralogist</i> 80, 21–26.",
                "10.2138/am-1995-1-203", "Structure of xenotime.", ["lattice"]),
        ],
        "cells": cells,
    }
