"""Magnetite: octahedron {111} <-> rhombic dodecahedron {110}, with cube / trapezohedron modifiers.

Rows   : {110} share of the {111}+{110} area (octahedron -> dodecahedron).
Columns: modifier form and its share of the total area: none, cube {100}, trapezohedron {311}.
"""

from ..habit import ABSENT, Crystal, Form, solve_pair, solve_share
from ..lattice import Lattice
from ._common import frac_text, ref

ID = "magnetite"
ROWS = [0.0, 0.25, 0.5, 0.75, 1.0]  # {110} share of {111}+{110}
COLS = [(None, 0.0), ("100", 0.1), ("311", 0.15)]
COL_TEXT = ["no modifier", "cube {100} ≈ 10%", "trapezohedron {311} ≈ 15%"]


def crystal() -> Crystal:
    return Crystal(
        "magnetite",
        Lattice(8.3941, 8.3941, 8.3941),
        "m-3m",
        [
            Form("111", (1, 1, 1), "octahedron o", "#3a3f4b"),
            Form("110", (1, 1, 0), "rhombic dodecahedron d", "#6b7a8f"),
            Form("100", (1, 0, 0), "cube a", "#a7b3c4"),
            Form("311", (3, 1, 1), "trapezohedron m", "#8f7a6b"),
        ],
        elongation_axis=None,
    )


def spec() -> dict:
    mt = crystal()
    cells = []
    for i, f110 in enumerate(ROWS):
        d0 = solve_pair(mt, {"111": 1.0, "110": 1.0, "100": ABSENT, "311": ABSENT}, "110", "111", f110)
        ref_key = "111" if d0.get("111") is not None else "110"
        for j, (mod, share) in enumerate(COLS):
            d = dict(d0)
            if mod:
                d = solve_share(mt, {**d, mod: d0[ref_key]}, mod, share, ref_key)
            cells.append({
                "id": f"M{i + 1}{'abc'[j]}", "row": i, "col": j, "label": f"M{i + 1}{'abc'[j]}",
                "description": f"{frac_text('{110}', '{111}', f110)}; {COL_TEXT[j]}.",
                "default": (i, j) == (1, 0), "distances": d, "t": 0.0,
            })
    return {
        "id": ID, "name": "Magnetite", "group": "Oxides", "crystal": mt, "formula": "Fe₃O₄",
        "chronometers": "(U–Th)/He; remanence carrier in paleomagnetism",
        "system": "Cubic", "setting": "Fd3̄m (spinel)",
        "lattice_source": "Fleet (1981)",
        "mono_color": "#3d4250",
        "view": {"tilt": 20, "turn": -28},
        "matrix": {
            "title": "Octahedron ↔ dodecahedron",
            "subtitle": "Rows run from the octahedron {111} to the rhombic dodecahedron {110}. Columns add cube {100} or trapezohedron {311} truncations.",
            "row_title": "{111} → {110}", "col_title": "Modifier",
            "rows": [{"label": f"M{i + 1}", "detail": frac_text("{110}", "{111}", f)} for i, f in enumerate(ROWS)],
            "cols": [{"label": "abc"[j], "detail": t} for j, t in enumerate(COL_TEXT)],
            "note": ("Form letters follow Dana (1892). m = {311} is taken from the spinel-group convention. No field study "
                     "systematically ties octahedral versus dodecahedral magnetite to temperature or fO₂. The best direct "
                     "evidence is experimental: Hirano &amp; Somiya (1976) found {110} gaining over {111} under more reducing "
                     "conditions. Spinel-law twins on {111} and biogenic habits are not modelled."),
        },
        "about": ABOUT,
        "habits": HABITS,
        "references": REFERENCES,
        "cells": cells,
    }


ABOUT = """
<p>Magnetite matters to two communities. It is a (U–Th)/He thermochronometer for mafic volcanic rocks and serpentinites,
and it is the main remanence carrier in paleomagnetism. Its habit is most commonly the octahedron o{111}. The rhombic
dodecahedron d{110} is the next most common and is often striated by o/d oscillation; the cube a{100} is rare (Dana 1892).
A BFDH ranking from the Fd3̄m reflection conditions predicts the same order, {111} &gt; {110} &gt; {311} &gt; {100}.</p>
<p>Grain shape matters for both uses. In (U–Th)/He dating, grain size and fragment geometry control α-ejection and
which population a date belongs to. In rock magnetism, elongation widens the single-domain size range, and truncated
octahedra are the standard shapes in micromagnetic models.</p>
"""

HABITS = [
    {"name": "Octahedral", "text": "o{111} alone or with small d truncations, the normal habit (rows M1–M2)."},
    {"name": "Dodecahedral", "text": "d{110} dominant, often striated parallel to the d/o edge (rows M4–M5)."},
    {"name": "Combinations", "text": "Octahedron plus dodecahedron, rarely cubo-octahedra (column b) or with m{311} (column c)."},
    {"name": "Not modelled", "text": "Spinel-law twins flattened on {111}, and biogenic or meteoritic habits (elongated prismatic, truncated hexa-octahedral)."},
]

REFERENCES = [
    ref("Fleet, M.E. (1981). The structure of magnetite. <i>Acta Crystallographica B</i> 37, 917–920.",
        "10.1107/S0567740881004597", "The cell used here (a = 8.3941 Å).", ["lattice"]),
    ref("Hirano, S., Somiya, S. (1976). Hydrothermal crystal growth of magnetite in the presence of hydrogen. <i>Journal of Crystal Growth</i> 35, 273–278.",
        "10.1016/0022-0248(76)90184-6", "Experiments in which {110} gains over {111} at higher H<sub>2</sub>, i.e. more reducing conditions. The clearest habit–condition link.", ["morphology"]),
    ref("Blackburn, T.J., Stockli, D.F., Walker, J.D. (2007). Magnetite (U–Th)/He dating and its application to the geochronology of intermediate to mafic volcanic rocks. <i>Earth and Planetary Science Letters</i> 259, 360–371.",
        "10.1016/j.epsl.2007.04.044", "The founding magnetite (U–Th)/He method. α-ejection is handled by air-abrading grain rims, so grain geometry enters directly.", ["thermochronology", "geometry"]),
    ref("Cooperdock, E.H.G., Stockli, D.F. (2016). Unraveling alteration histories in serpentinites and associated ultramafic rocks with magnetite (U-Th)/He geochronology. <i>Geology</i> 44, 967–970.",
        "10.1130/G38587.1", "Interior fragments of large grains record cooling, while small grains record later hydrothermal growth. Grain size and geometry guide interpretation.", ["thermochronology", "geometry"]),
    ref("Schwartz, S., Gautheron, C., Ketcham, R.A., et al. (2020). Unraveling the exhumation history of high-pressure ophiolites using magnetite (U-Th-Sm)/He thermochronometry. <i>Earth and Planetary Science Letters</i> 543, 116359.",
        "10.1016/j.epsl.2020.116359", "Euhedral and pseudo-euhedral grain shapes give distinct date populations.", ["thermochronology", "geometry"]),
    ref("Fanale, F.P., Kulp, J.L. (1962). The helium method and the age of the Cornwall, Pennsylvania magnetite ore. <i>Economic Geology</i> 57, 735–746.",
        "10.2113/gsecongeo.57.5.735", "The earliest helium dating of magnetite.", ["thermochronology"]),
    ref("Butler, R.F., Banerjee, S.K. (1975). Theoretical single-domain grain size range in magnetite and titanomagnetite. <i>Journal of Geophysical Research</i> 80, 4049–4058.",
        "10.1029/JB080i029p04049", "Elongation widens the single-domain size range, so grain shape controls remanence stability.", ["paleomagnetism", "geometry"]),
    ref("Muxworthy, A.R., Williams, W. (2006). Critical single-domain/multidomain grain sizes in noninteracting and interacting elongated magnetite particles. <i>Journal of Geophysical Research: Solid Earth</i> 111.",
        "10.1029/2006JB004588", "Micromagnetic SD/MD thresholds as a function of particle elongation.", ["paleomagnetism", "geometry"]),
    ref("Nagy, L., Williams, W., Muxworthy, A.R., Fabian, K., Almeida, T.P., Ó Conbhuí, P., Shcherbakov, V.P. (2017). Stability of equidimensional pseudo-single-domain magnetite over billion-year timescales. <i>PNAS</i> 114, 10356–10360.",
        "10.1073/pnas.1708344114", "Vortex-state equant grains are stable remanence carriers.", ["paleomagnetism"]),
    ref("Devouard, B., Pósfai, M., Hua, X., Bazylinski, D.A., Frankel, R.B., Buseck, P.R. (1998). Magnetite from magnetotactic bacteria: size distributions and twinning. <i>American Mineralogist</i> 83, 1387–1398.",
        "10.2138/am-1998-11-1228", "Quantitative size, shape and twin statistics of biologically controlled magnetite.", ["morphology"]),
    ref("Thomas-Keprta, K.L., Clemett, S.J., Bazylinski, D.A., et al. (2001). Truncated hexa-octahedral magnetite crystals in ALH84001: Presumptive biosignatures. <i>PNAS</i> 98, 2164–2169.",
        "10.1073/pnas.051500898", "Crystal habit used as a diagnostic of how the magnetite formed.", ["morphology"]),
    ref("Dunlop, D.J., Özdemir, Ö. (1997). <i>Rock Magnetism: Fundamentals and Frontiers</i>. Cambridge University Press.",
        "10.1017/CBO9780511612794", "Reference text on grain size, shape and domain state.", ["paleomagnetism", "review"]),
]
