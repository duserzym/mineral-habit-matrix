"""Apatite: termination type x elongation.

Rows   : termination, from flat basal {0001} to fully pyramidal {10-11}.
Columns: length/width aspect ratio, from stubby to acicular.

Termination share = {0001} fraction of the termination area.  The prism is the
first-order hexagonal prism {10-10}.
"""

from ..habit import Crystal, Form
from ..lattice import Lattice
from ._common import ref, prism_then_cap

ID = "apatite"
ROWS = [  # (label, detail, {0001} share of the termination area)
    ("basal", "{0001} only", 1.0),
    ("basal ≫ pyr.", "{0001} > {10-11}", 0.65),
    ("pyr. > basal", "{10-11} > {0001}", 0.25),
    ("pyramidal", "{10-11} only", 0.0),
]
ASPECTS = [1.0, 1.5, 2.5, 4.0, 7.0]


def crystal() -> Crystal:
    return Crystal(
        "apatite",
        Lattice(9.3973, 9.3973, 6.8782, 90, 90, 120),
        "6/m",
        [
            Form("10-10", (1, 0, -1, 0), "first-order prism m", "#5f9ea0"),
            Form("0001", (0, 0, 0, 1), "basal pinacoid c", "#e0c060"),
            Form("10-11", (1, 0, -1, 1), "first-order pyramid x", "#b0647a"),
        ],
        elongation_axis=(0, 0, 1),
    )


def spec() -> dict:
    ap = crystal()
    base = {"10-10": 1.0, "0001": 1.0, "10-11": 1.0}
    cells = []
    for i, (rl, rd, fc) in enumerate(ROWS):
        for j, asp in enumerate(ASPECTS):
            d, t = prism_then_cap(ap, base, None, ("0001", "10-11", fc), asp)
            cells.append({
                "id": f"T{i + 1}_A{asp:g}", "row": i, "col": j, "label": f"T{i + 1}·{asp:g}", "sub": "",
                "description": f"Termination: {rd}. Aspect ratio {asp:g}:1.",
                "default": (i, j) == (2, 2), "distances": d, "t": t,
            })
    return {
        "id": ID, "name": "Apatite", "crystal": ap, "formula": "Ca₅(PO₄)₃(F,Cl,OH)",
        "chronometers": "(U–Th)/He, fission track, U–Pb, Sm–Nd",
        "system": "Hexagonal", "setting": "P6₃/m (fluorapatite)",
        "lattice_source": "Hughes et al. (1989)",
        "mono_color": "#7fb3a8",
        "matrix": {
            "title": "Termination × elongation",
            "subtitle": "Prism {10-10}. Rows run from a flat basal pinacoid to a pyramidal termination. Columns run from stubby to acicular habits.",
            "row_title": "Termination", "col_title": "Aspect ratio (L/W)",
            "rows": [{"label": f"T{i + 1} · {r[0]}", "detail": r[1]} for i, r in enumerate(ROWS)],
            "cols": [{"label": f"{a:g}", "detail": ""} for a in ASPECTS],
            "note": "",
        },
        "about": ABOUT,
        "habits": HABITS,
        "references": REFERENCES,
        "cells": cells,
    }


ABOUT = """
<p>Apatite is the main low-temperature thermochronometer, for (U–Th)/He and fission track, and its grain geometry
enters every age. The α-ejection correction F<sub>T</sub> depends on the surface-to-volume ratio of an idealized
hexagonal prism with 0, 1 or 2 pyramidal terminations. Micro-CT studies show that 2D microscope measurements
overestimate volume and surface area by about 20–25 %.</p>
<p>Habit also records growth conditions. Acicular, often hollow, apatite forms under rapid cooling or quench, and
stubby prisms form under slower growth (Wyllie et al. 1962; Piccoli &amp; Candela 2002). This relation is
qualitative, and no Pupin-style apatite typology has been published. The matrix spans the two geometric variables
that matter for F<sub>T</sub>: termination type and elongation.</p>
"""

HABITS = [
    {"name": "Prismatic, pyramid-terminated", "text": "m{10-10} with x{10-11} terminations and little or no c{0001}. The common igneous habit (rows 3–4)."},
    {"name": "Stubby / equant", "text": "m ≈ x, with or without c. Slow, near-equilibrium growth (columns 1–2)."},
    {"name": "Acicular", "text": "Very long m (10–20:1 or more) with c or x ends, often hollow. Quench or strong undercooling (column 5 is a mild version)."},
    {"name": "Tabular on {0001}", "text": "c dominant with short m. Pegmatitic or hydrothermal; small s{11-21} and r{10-12} faces are not modelled."},
]

REFERENCES = [
    ref("Wyllie, P.J., Cox, K.G., Biggar, G.M. (1962). The habit of apatite in synthetic systems and igneous rocks. <i>Journal of Petrology</i> 3, 238–243.",
        "10.1093/petrology/3.2.238", "The classic link between acicular apatite and rapid cooling, and between stubby apatite and slower growth.", ["morphology"]),
    ref("Piccoli, P.M., Candela, P.A. (2002). Apatite in igneous systems. <i>Reviews in Mineralogy and Geochemistry</i> 48, 255–292.",
        "10.2138/rmg.2002.48.6", "Reviews apatite habit versus undercooling, including skeletal and hollow quench crystals about 20:1.", ["morphology", "review"]),
    ref("Webster, J.D., Piccoli, P.M. (2015). Magmatic apatite: a powerful, yet deceptive, mineral. <i>Elements</i> 11, 177–182.",
        "10.2113/gselements.11.3.177", "Overview of magmatic apatite.", ["review"]),
    ref("Farley, K.A., Wolf, R.A., Silver, L.T. (1996). The effects of long alpha-stopping distances on (U-Th)/He ages. <i>Geochimica et Cosmochimica Acta</i> 60, 4223–4229.",
        "10.1016/S0016-7037(96)00193-7", "The original geometry-based F<sub>T</sub> correction.", ["thermochronology", "geometry"]),
    ref("Ketcham, R.A., Gautheron, C., Tassan-Got, L. (2011). Accounting for long alpha-particle stopping distances in (U–Th–Sm)/He geochronology: refinement of the baseline case. <i>Geochimica et Cosmochimica Acta</i> 75, 7779–7791.",
        "10.1016/j.gca.2011.10.011", "Standard F<sub>T</sub> equations for idealized crystal shapes.", ["thermochronology", "geometry"]),
    ref("Cooperdock, E.H.G., Ketcham, R.A., Stockli, D.F. (2019). Resolving the effects of 2-D versus 3-D grain measurements on apatite (U–Th)/He age data and reproducibility. <i>Geochronology</i> 1, 17–41.",
        "10.5194/gchron-1-17-2019", "From micro-CT, 2D measurement overestimates volume and surface area by about 20–25 %.", ["thermochronology", "geometry"]),
    ref("Glotzbach, C., Lang, K.A., Avdievitch, N.N., Ehlers, T.A. (2019). Increasing the accuracy of (U-Th(-Sm))/He dating with 3D grain modelling. <i>Chemical Geology</i> 506, 113–125.",
        "10.1016/j.chemgeo.2018.12.032", "3D grain models for He dating.", ["thermochronology", "geometry"]),
    ref("Zeigler, S.D., Metcalf, J.R., Flowers, R.M. (2023). A practical method for assigning uncertainty and improving the accuracy of alpha-ejection corrections and eU concentrations in apatite (U–Th)/He chronology. <i>Geochronology</i> 5, 197–228.",
        "10.5194/gchron-5-197-2023", "Geometry-based uncertainty in F<sub>T</sub> and eU.", ["thermochronology", "geometry"]),
    ref("Evans, N.J., McInnes, B.I.A., Squelch, A.P., Austin, P.J., McDonald, B.J., Wu, Q. (2008). Application of X-ray micro-computed tomography in (U–Th)/He thermochronology. <i>Chemical Geology</i> 257, 101–113.",
        "10.1016/j.chemgeo.2008.08.021", "Micro-CT measurement of grain geometry.", ["geometry"]),
    ref("Herman, F., Braun, J., Senden, T.J., Dunlap, W.J. (2007). (U–Th)/He thermochronometry: mapping 3D geometry using micro-X-ray tomography and solving the associated production–diffusion equation. <i>Chemical Geology</i> 242, 126–136.",
        "10.1016/j.chemgeo.2007.03.009", "Production–diffusion modelling on 3D grain geometry.", ["geometry"]),
    ref("Brown, R.W. et al. (2013). Natural age dispersion arising from the analysis of broken crystals. Part I: Theoretical basis and implications for the apatite (U–Th)/He thermochronometer. <i>Geochimica et Cosmochimica Acta</i> 122, 478–497.",
        "10.1016/j.gca.2013.05.041", "Shows how missing terminations bias He ages.", ["thermochronology", "geometry"]),
    ref("Flowers, R.M. et al. (2023). (U-Th)/He chronology: Part 1. Data, uncertainty, and reporting. <i>GSA Bulletin</i> 135, 104–136.",
        "10.1130/B36266.1", "Community reporting standards for F<sub>T</sub> and grain geometry.", ["thermochronology"]),
    ref("Hughes, J.M., Cameron, M., Crowley, K.D. (1989). Structural variations in natural F, OH, and Cl apatites. <i>American Mineralogist</i> 74, 870–876.",
        None, "The fluorapatite cell used here (a = 9.397, c = 6.878 Å).", ["lattice"], url="http://www.minsocam.org/ammin/AM74/AM74_870.pdf"),
]
