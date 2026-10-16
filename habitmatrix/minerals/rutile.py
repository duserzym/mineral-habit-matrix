"""Rutile: a Pupin-style prism x pyramid grid on the rutile lattice.

Rutile is tetragonal like zircon, but its common forms are the prism {110} (dominant),
the second prism {100}, and the terminations {101} and {111}.

Rows   : {111} share of the termination area (dipyramid {101} -> {111}).
Columns: {100} share of the prism cross-section ({110} -> {100}).
"""

from ..habit import Crystal, Form
from ..lattice import Lattice
from ._common import ref, frac_text, prism_then_cap

ID = "rutile"
ASPECT = 3.5
PRISM = [0.0, 0.2, 0.4, 0.6]  # {100} share of the prism perimeter
CAP = [0.0, 0.3, 0.6, 1.0]    # {111} share of the termination area


def crystal() -> Crystal:
    return Crystal(
        "rutile",
        Lattice(4.5937, 4.5937, 2.9587),
        "4/mmm",
        [
            Form("110", (1, 1, 0), "prism m", "#9c3d2e"),
            Form("100", (1, 0, 0), "prism a", "#d38b4c"),
            Form("101", (1, 0, 1), "dipyramid e", "#5d7f99"),
            Form("111", (1, 1, 1), "dipyramid s", "#8aa86b"),
        ],
        elongation_axis=(0, 0, 1),
    )


def spec() -> dict:
    rt = crystal()
    base = {"110": 1.0, "100": 1.0, "101": 1.2, "111": 1.2}
    cells = []
    for i, fc in enumerate(CAP):
        for j, fp in enumerate(PRISM):
            d, t = prism_then_cap(rt, base, ("110", "100", 1 - fp), ("111", "101", fc), ASPECT)
            cells.append({
                "id": f"P{j + 1}_T{i + 1}", "row": i, "col": j, "label": f"P{j + 1}·T{i + 1}",
                "description": (f"Prism: {frac_text('{110}', '{100}', 1 - fp)}. "
                                f"Termination: {frac_text('{111}', '{101}', fc)}."),
                "default": (i, j) == (1, 1), "distances": d, "t": t,
            })
    return {
        "id": ID, "name": "Rutile", "group": "Accessory chronometers", "crystal": rt, "formula": "TiO₂",
        "chronometers": "U–Pb, Zr-in-rutile thermometry, (U–Th)/He",
        "system": "Tetragonal", "setting": "P4₂/mnm",
        "lattice_source": "Handbook of Mineralogy",
        "mono_color": "#a4553a",
        "matrix": {
            "title": "Prism × termination grid",
            "subtitle": "This is a Pupin-style grid on the rutile cell. Columns run from the {110} prism to a mixed {110}+{100} prism. Rows run from {101} to {111} terminations.",
            "row_title": "Termination", "col_title": "Prism",
            "rows": [{"label": f"T{i + 1}", "detail": frac_text("{111}", "{101}", f)} for i, f in enumerate(CAP)],
            "cols": [{"label": f"P{j + 1}", "detail": frac_text("{110}", "{100}", 1 - f)} for j, f in enumerate(PRISM)],
            "note": "",
        },
        "about": ABOUT,
        "habits": HABITS,
        "references": REFERENCES,
        "cells": cells,
    }


ABOUT = """
<p>Rutile is tetragonal like zircon, but its habit is dominated by the {110} prism with a subordinate {100} prism and
{101} and {111} dipyramid terminations. Rutile ranges from equant to acicular, including needles exsolved in garnet
and quartz. Rutile U–Pb and Zr-in-rutile thermometry are central to metamorphic petrochronology. Grain size and shape
set the Pb diffusion domain. No Pupin-style typology for rutile has been published, so this grid uses Pupin's
prism × termination layout on the rutile cell.</p>
"""

HABITS = [
    {"name": "Prismatic", "text": "m{110} (± a{100}) elongated along c, with e{101} and/or s{111} terminations."},
    {"name": "Acicular / needles", "text": "Extreme m elongation. Sagenite in quartz and oriented exsolution needles in garnet."},
    {"name": "Equant / dipyramidal", "text": "e + s with a short prism."},
    {"name": "Geniculate twins (not modelled)", "text": "Elbow twins on {101} and reticulate twins on {301} are not convex."},
]

REFERENCES = [
    ref("Zack, T., Kooijman, E. (2017). Petrology and geochronology of rutile. <i>Reviews in Mineralogy and Geochemistry</i> 83, 443–467.",
        "10.2138/rmg.2017.83.14", "The standard review of rutile petrochronology.", ["review"]),
    ref("Meinhold, G. (2010). Rutile and its applications in earth sciences. <i>Earth-Science Reviews</i> 102, 1–28.",
        "10.1016/j.earscirev.2010.06.001", "Covers occurrence, habit and provenance.", ["review", "morphology"]),
    ref("Cherniak, D.J. (2000). Pb diffusion in rutile. <i>Contributions to Mineralogy and Petrology</i> 139, 198–207.",
        "10.1007/PL00007671", "Diffusion data for grain-size and closure modelling.", ["diffusion"]),
    ref("Kooijman, E., Mezger, K., Berndt, J. (2010). Constraints on the U–Pb systematics of metamorphic rutile from in situ LA-ICP-MS analysis. <i>Earth and Planetary Science Letters</i> 293, 321–330.",
        "10.1016/j.epsl.2010.02.047", "Grain-scale U–Pb profiles used to study diffusion and closure.", ["geochronology", "geometry"]),
    ref("Ague, J.J., Eckert, J.O. (2012). Precipitation of rutile and ilmenite needles in garnet: implications for extreme metamorphic conditions in the Acadian Orogen, U.S.A. <i>American Mineralogist</i> 97, 840–855.",
        "10.2138/am.2012.4015", "Links needle morphology and orientation to ultrahigh-temperature conditions.", ["morphology"]),
    ref("Proyer, A. et al. (2013). TiO₂ exsolution from garnet by open-system precipitation: evidence from crystallographic and shape preferred orientation of rutile inclusions. <i>Contributions to Mineralogy and Petrology</i> 166, 211–234.",
        "10.1007/s00410-013-0872-7", "Rutile inclusion shape and orientation as a record of the precipitation process.", ["morphology"]),
    ref("Swope, R.J., Smyth, J.R., Larson, A.C. (1995). H in rutile-type compounds: I. Single-crystal neutron and X-ray diffraction study of H in rutile. <i>American Mineralogist</i> 80, 448–453.",
        "10.2138/am-1995-5-604", "Rutile structure refinement.", ["lattice"]),
]
