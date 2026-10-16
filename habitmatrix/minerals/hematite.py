"""Hematite: rhombohedral -> tabular (specular) habits.

Setting: R3̄c, obverse hexagonal axes (a = 5.0355, c = 13.7471 Å; Maslen et al. 1994), point
group 3̄ 2/m with 2-folds along the a axes (-3m1).  Classical morphology (Dana 1892) uses a
cell with c halved (c/a = 1.3656); converting (hkil) -> (hki,2l) and choosing the
obverse-consistent sign gives
    c{0001} -> {0001},  r{10-11} -> {01-12},  e{01-12} -> {10-14},  n{22-43} -> {11-23}.
Check: r∧r' = 93.99° and c∧r = 57.61° here, against Dana's 94°0' and 57°37'.

Rows   : thickness / width along c (rhombohedral, no basal face -> thin specular plates).
Columns: forms bevelling the plate edges: r only, r + e{10-14}, r + n{11-23}.
"""

from ..habit import ABSENT, Crystal, Form, solve_aspect, solve_share
from ..lattice import Lattice
from ._common import ref

ID = "hematite"
ROWS = [None, 0.6, 0.3, 0.12]  # None = rhombohedron without basal pinacoid
ROW_TEXT = ["rhombohedral", "thick tabular", "tabular", "specular plate"]
COLS = [(None, 0.0), ("10-14", 0.35), ("11-23", 0.35)]  # (edge form, its share of r + edge area)
COL_TEXT = ["r{011̄2} only", "r + e{101̄4}", "r + n{112̄3}"]


def crystal() -> Crystal:
    return Crystal(
        "hematite",
        Lattice(5.0355, 5.0355, 13.7471, 90, 90, 120),
        "-3m",
        [
            Form("0001", (0, 0, 0, 1), "c, basal pinacoid", "#5b2a2a"),
            Form("01-12", (0, 1, -1, 2), "r, rhombohedron (Dana {101̄1})", "#a3402f"),
            Form("10-14", (1, 0, -1, 4), "e, rhombohedron (Dana {011̄2})", "#d08a5c"),
            Form("11-23", (1, 1, -2, 3), "n, dipyramid (Dana {224̄3})", "#7d5a6e"),
        ],
        elongation_axis=(0, 0, 1),
    )


def spec() -> dict:
    hm = crystal()
    cells = []
    for i, th in enumerate(ROWS):
        for j, (edge, share) in enumerate(COLS):
            d = {"0001": ABSENT, "01-12": 1.0, "10-14": ABSENT, "11-23": ABSENT}
            if edge:
                d = solve_share(hm, {**d, edge: 1.0}, edge, share, "01-12", among=["01-12", edge], t=0.0)
            t = 0.0
            if th is not None:
                # thin the plate, then re-balance the edge forms on the plate's rim (the basal face
                # can cut shallow edge forms away entirely), then re-solve the thickness
                d["0001"] = 0.05
                t = solve_aspect(hm, d, th)
                if edge:
                    d = solve_share(hm, d, edge, share, "01-12", among=["01-12", edge], t=t)
                    t = solve_aspect(hm, d, th)
            cells.append({
                "id": f"H{i + 1}{'abc'[j]}", "row": i, "col": j, "label": f"H{i + 1}{'abc'[j]}",
                "description": f"{ROW_TEXT[i].capitalize()}" + ("" if th is None else f" (thickness:width ≈ 1:{1 / th:.1f})") + f"; {COL_TEXT[j]}.",
                "default": (i, j) == (2, 0), "distances": d, "t": t,
            })
    return {
        "id": ID, "name": "Hematite", "crystal": hm, "formula": "α-Fe₂O₃",
        "chronometers": "(U–Th)/He, (U–Th)/Ne; remanence carrier in paleomagnetism",
        "system": "Trigonal", "setting": "R3̄c, obverse hexagonal axes",
        "lattice_source": "Maslen et al. (1994)",
        "mono_color": "#4a2626",
        "view": {"tilt": 28, "turn": -20},
        "matrix": {
            "title": "Rhombohedral → specular plates",
            "subtitle": "Rows flatten the crystal on the basal pinacoid c{0001}. Columns change the forms that bevel the plate edges.",
            "row_title": "Thickness", "col_title": "Edge forms",
            "rows": [{"label": f"H{i + 1}", "detail": ROW_TEXT[i] + ("" if t is None else f" · 1:{1 / t:.0f}")} for i, t in enumerate(ROWS)],
            "cols": [{"label": "abc"[j], "detail": t} for j, t in enumerate(COL_TEXT)],
            "note": ("Indices use the structural R3̄c cell. Dana (1892) and most older literature use a morphological cell "
                     "with c halved. The conversion was checked against Dana's interfacial angles (r∧r′ = 94°0′, "
                     "c∧r = 57°37′), but the obverse/reverse sign is our derivation. No field study systematically ties "
                     "hematite habit to temperature or fO₂, so the rows describe shapes, not conditions. Twins, rosettes "
                     "(iron roses) and botryoidal aggregates are not modelled."),
        },
        "about": ABOUT,
        "habits": HABITS,
        "references": REFERENCES,
        "cells": cells,
    }


ABOUT = """
<p>Hematite is a (U–Th)/He thermochronometer for fault zones, veins and iron formations, and a remanence carrier in
paleomagnetism. Its habit matters directly for chronometry, because the individual crystal acts as the He diffusion
domain. Thick specularite plates retain He to higher temperatures than fine platelets or the micron-scale crystallites
of botryoidal hematite (Bähr et al. 1994; Farley 2018; Evenson et al. 2014).</p>
<p>Structure alone predicts a rhombohedral habit dominated by r{011̄2}. The common tabular habit on {0001} (specularite,
micaceous hematite, iron roses) therefore reflects growth conditions, such as hydrothermal growth above about 100 °C
for coarse grey specular hematite (Catling &amp; Moore 2003).</p>
"""

HABITS = [
    {"name": "Tabular / specular", "text": "c{0001} dominant, with edges bevelled by r, e, u and n (rows H2–H4)."},
    {"name": "Rhombohedral", "text": "r dominant, the near-cubic rhombohedron (r∧r′ = 94°). Rare as a free habit (row H1)."},
    {"name": "Micaceous / iron rose", "text": "Very thin laminae parallel to c, single or in rosettes. Rosettes are not modelled."},
    {"name": "Not modelled", "text": "Penetration twins on {0001}, lamellar twins on r, prismatic and scalenohedral crystals, botryoidal masses, and martite (hematite pseudomorphs after magnetite)."},
]

REFERENCES = [
    ref("Bähr, R., Lippolt, H.J., Wernicke, R.S. (1994). Temperature-induced <sup>4</sup>He degassing of specularite and botryoidal hematite: A <sup>4</sup>He retentivity study. <i>Journal of Geophysical Research: Solid Earth</i> 99, 17695–17707.",
        "10.1029/94JB01055", "The diffusion length matches the macroscopic grain in specularite but the 0.1–10 µm crystallites in botryoidal hematite. Habit sets He retention.", ["thermochronology", "geometry"]),
    ref("Wernicke, R.S., Lippolt, H.J. (1994). Dating of vein specularite using internal (U+Th)/<sup>4</sup>He isochrons. <i>Geophysical Research Letters</i> 21, 345–347.",
        "10.1029/94GL00014", "Early (U–Th)/He dating of the tabular specular habit.", ["thermochronology"]),
    ref("Farley, K.A., Flowers, R.M. (2012). (U–Th)/Ne and multidomain (U–Th)/He systematics of a hydrothermal hematite from eastern Grand Canyon. <i>Earth and Planetary Science Letters</i> 359–360, 131–140.",
        "10.1016/j.epsl.2012.10.010", "Multi-domain He diffusion in polycrystalline hydrothermal hematite.", ["thermochronology"]),
    ref("Evenson, N.S., Reiners, P.W., Spencer, J.E., Shuster, D.L. (2014). Hematite and Mn oxide (U-Th)/He dates from the Buckskin-Rawhide detachment system, western Arizona. <i>American Journal of Science</i> 314, 1373–1435.",
        "10.2475/10.2014.01", "Crystal size controls He retentivity. Closure temperatures of about 140–240 °C come from measured crystal sizes.", ["thermochronology", "geometry"]),
    ref("Farley, K.A. (2018). Helium diffusion parameters of hematite from a single-diffusion-domain crystal. <i>Geochimica et Cosmochimica Acta</i> 231, 117–129.",
        "10.1016/j.gca.2018.04.005", "The physical crystal is the diffusion domain (E<sub>a</sub> ≈ 170 kJ/mol).", ["thermochronology", "geometry"]),
    ref("Jensen, J.L., Siddoway, C.S., Reiners, P.W., Ault, A.K., Thomson, S.N., Steele-MacInnis, M. (2018). Single-crystal hematite (U–Th)/He dates and fluid inclusions document widespread Cryogenian sand injection in crystalline basement. <i>Earth and Planetary Science Letters</i> 500, 145–155.",
        "10.1016/j.epsl.2018.08.021", "Individual crystals within aggregates are the diffusion domains, and closure temperature rises with crystal size.", ["thermochronology", "geometry"]),
    ref("Ault, A.K., Reiners, P.W., Evans, J.P., Thomson, S.N. (2015). Linking hematite (U-Th)/He dating with the microtextural record of seismicity in the Wasatch fault damage zone, Utah, USA. <i>Geology</i> 43, 771–774.",
        "10.1130/G36897.1", "Fault-surface hematite textures linked to He dates reset by frictional heating.", ["thermochronology", "texture"]),
    ref("Ault, A.K., Gautheron, C., King, G.E. (2019). Innovations in (U–Th)/He, fission track, and trapped charge thermochronometry with applications to earthquakes, weathering, surface-mantle connections, and the growth and decay of mountains. <i>Tectonics</i> 38, 3705–3739.",
        "10.1029/2018TC005312", "Review that includes hematite thermochronometry.", ["review"]),
    ref("Catling, D.C., Moore, J.M. (2003). The nature of coarse-grained crystalline hematite and its implications for the early environment of Mars. <i>Icarus</i> 165, 277–300.",
        "10.1016/S0019-1035(03)00173-8", "Coarse specular hematite generally needs to crystallize above about 100 °C. A habit–condition link.", ["morphology"]),
    ref("Lane, M.D., Morris, R.V., Mertzman, S.A., Christensen, P.R. (2002). Evidence for platy hematite grains in Sinus Meridiani, Mars. <i>Journal of Geophysical Research: Planets</i> 107.",
        "10.1029/2001JE001832", "Thermal emission dominated by the c-face, implying platy {0001} grains.", ["morphology"]),
    ref("Maslen, E.N., Streltsov, V.A., Streltsova, N.R., Ishizawa, N. (1994). Synchrotron X-ray study of the electron density in α-Fe<sub>2</sub>O<sub>3</sub>. <i>Acta Crystallographica B</i> 50, 435–441.",
        "10.1107/S0108768194002284", "The cell used here (a = 5.0355, c = 13.7471 Å).", ["lattice"]),
]
