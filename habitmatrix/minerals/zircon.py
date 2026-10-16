"""Zircon: the Pupin (1980) typology grid (64 cells, 66 subtype labels).

Layout follows Pupin (1980, Fig. 1) as reproduced by Osorio-Granada et al. (2017, Fig. 4)
and Daneshvar et al. (2018, Fig. 5):

Columns I.A (100..800), pyramids:  {211} only, {101}<<{211}, {101}<{211}, {101}={211},
                                   {101}>{211}, {101}>>{211}, {101} only, steep {301}
Rows    I.T (100..800), prisms:    no prism, {110} only, {100}<<{110}, {100}<{110},
                                   {100}={110}, {100}>{110}, {100}>>{110}, {100} only
I.T is read as an estimated crystallization temperature of ~550..900 °C (±50 °C).

Pupin judged face development visually.  The five mixed steps of each index are mapped
to evenly spaced fractions 1/6..5/6 of
  * the {100} share of the prism cross-section perimeter (I.T), and
  * the {101} share of the pyramid surface area (I.A).
"""

from ..habit import ABSENT, Crystal, Form
from ..lattice import Lattice
from ._common import frac_text, prism_then_cap, ref

ID = "zircon"
ASPECT = 2.5        # length / width of prismatic types; the typology does not use elongation
ASPECT_301 = 3.6    # the steep {301} types are drawn longer (they cannot be shorter than ~2.7)
INDEX = [100 * (i + 1) for i in range(8)]
MIX = [k / 6 for k in range(1, 6)]

# rows: I.T -> {100} share of the prism (None = no prism)
IT_PRISM = [None, 0.0] + MIX + [1.0]
IT_TEXT = ["no prism", "{110} only", "{100} ≪ {110}", "{100} < {110}", "{100} = {110}",
           "{100} > {110}", "{100} ≫ {110}", "{100} only"]
IT_TEMP = [500 + v // 2 for v in INDEX]  # 550..900 °C
# cols: I.A -> {101} share of the pyramid ("301" = the steep {301} pyramid alone)
IA_PYR = [0.0] + MIX + [1.0, "301"]
IA_TEXT = ["{211} only", "{101} ≪ {211}", "{101} < {211}", "{101} = {211}", "{101} > {211}",
           "{101} ≫ {211}", "{101} only", "{301}"]

SUBTYPES = [  # [I.T row][I.A column]
    ["B", "AB1", "AB2", "AB3", "AB4", "AB5", "A", "C"],
    ["H", "L1", "L2", "L3", "L4", "L5", "G1", "I"],
    ["Q1", "S1", "S2", "S3", "S4", "S5", "P1", "R1"],
    ["Q2", "S6", "S7", "S8", "S9", "S10", "P2", "R2"],
    ["Q3", "S11", "S12", "S13", "S14", "S15", "P3", "R3"],
    ["Q4", "S16", "S17", "S18", "S19", "S20", "P4", "R4"],
    ["Q5", "S21", "S22", "S23", "S24", "S25", "P5", "R5"],
    ["E", "J1", "J2", "J3", "J4", "J5", "D", "F"],
]


def crystal() -> Crystal:
    return Crystal(
        "zircon",
        Lattice(6.607, 6.607, 5.982),
        "4/mmm",
        [
            Form("100", (1, 0, 0), "prism", "#d9a441"),
            Form("110", (1, 1, 0), "prism", "#b5562f"),
            Form("101", (1, 0, 1), "pyramid", "#6f8fb3"),
            Form("211", (2, 1, 1), "pyramid", "#7a9e6a"),
            Form("301", (3, 0, 1), "steep pyramid", "#9a7bb0"),
        ],
        elongation_axis=(0, 0, 1),
    )


def _distances(zr, prism, pyr):
    base = {"100": 1.0, "110": 1.0, "101": 1.2, "211": 1.2, "301": ABSENT}
    if pyr == "301":
        base.update({"101": ABSENT, "211": ABSENT, "301": 0.95})
        cap = None
    else:
        cap = ("101", "211", pyr)
    if prism is None:  # bipyramid: no prism faces, caps meet
        base.update({"100": ABSENT, "110": ABSENT})
        return prism_then_cap(zr, base, None, cap, None, cap_t=0.0)
    return prism_then_cap(zr, base, ("100", "110", prism), cap, ASPECT_301 if pyr == "301" else ASPECT)


def spec() -> dict:
    zr = crystal()
    cells = []
    for i, prism in enumerate(IT_PRISM):      # rows: I.T
        for j, pyr in enumerate(IA_PYR):      # cols: I.A
            d, t = _distances(zr, prism, pyr)
            name = SUBTYPES[i][j]
            extra = " G2 and G3 (small, near-equant variants in the same cell) are not modelled." if name == "G1" else ""
            cells.append({
                "id": name, "row": i, "col": j, "label": name, "sub": "",
                "title": f"{name}: I.A {INDEX[j]}, I.T {INDEX[i]}",
                "description": (f"I.A = {INDEX[j]}: {IA_TEXT[j]}. I.T = {INDEX[i]}: {IT_TEXT[i]} "
                                f"(~{IT_TEMP[i]} °C after Pupin 1980).{extra}"),
                "default": name == "S13",
                "distances": d, "t": t,
            })
    return {
        "id": ID, "name": "Zircon", "group": "Accessory chronometers", "crystal": zr, "formula": "ZrSiO₄",
        "chronometers": "U–Pb, (U–Th)/He, fission track, Lu–Hf, Ti-in-zircon",
        "system": "Tetragonal", "setting": "I4₁/amd (structural cell; Pupin's indices)",
        "lattice_source": "Robinson et al. (1971)",
        "mono_color": "#c98d5b",
        "matrix": {
            "title": "Pupin (1980) typology grid",
            "subtitle": ("Columns: I.A, the pyramid index, which reflects melt Al/(Na+K). Rows: I.T, the prism index, "
                         "which Pupin read as a crystallization temperature."),
            "row_title": "I.T · prisms · T",
            "col_title": "I.A · pyramids",
            "rows": [{"label": str(v), "detail": f"{IT_TEXT[i]} · {IT_TEMP[i]} °C"} for i, v in enumerate(INDEX)],
            "cols": [{"label": str(v), "detail": IA_TEXT[j]} for j, v in enumerate(INDEX)],
            "note": ("The layout follows Pupin (1980, Fig. 1) as reproduced by Osorio-Granada et al. (2017) and Daneshvar "
                     "et al. (2018). The temperature scale is Pupin's ±50 °C estimate. Mixed steps are spaced evenly as "
                     "1/6–5/6 of the prism perimeter or pyramid area. Pupin's ratios are visual, so this spacing is a "
                     "modelling choice and not part of the original definition. Prismatic types are drawn at 2.5:1 and the "
                     "{301} types at 3.6:1."),
        },
        "about": ABOUT,
        "habits": HABITS,
        "references": REFERENCES,
        "cells": cells,
    }


ABOUT = """
<p>Pupin (1980) sorted accessory zircon from granitoids into 64 cells (S1–S25, L, G, P, Q, R, J, AB and the single-letter
types) using two indices.</p>
<ul>
<li><strong>I.A</strong> (columns) records the relative development of the pyramids {211} and {101}, plus the steep {301}. Pupin read
it as an index of the melt's Al/(Na+K) balance.</li>
<li><strong>I.T</strong> (rows) records the prisms, from none, to {110} only, to {100} only. Pupin read it as a crystallization
temperature from about 550 to 900 °C.</li>
</ul>
<p>The mean point (Ā, T̄) and the typological evolution trend of a zircon population fall in fields for crustal,
hybrid and mantle-derived granites.</p>
<p>Every crystal in the matrix uses the real zircon cell (c/a = 0.905), so all interfacial angles are genuine zircon
angles. Only the central distances of the five forms change from cell to cell. The temperature reading of I.T is
contested. Benisek &amp; Finger (1993) showed that trace-element uptake on {110} also controls prism development, so use
the T axis as Pupin's calibration, not as a thermometer.</p>
"""

HABITS = [
    {"name": "Crustal (aluminous) granites",
     "text": "Low I.A, about 150–350, and I.T about 300–450. S1–S7, L and Q types dominate: {211}-rich pyramids on {110}-rich prisms. This covers aluminous leucogranites and (sub)autochthonous and intrusive aluminous monzogranites and granodiorites."},
    {"name": "Hybrid (crust + mantle) granites",
     "text": "Calc-alkaline and high-K calc-alkaline granodiorites and monzonites at I.A about 400–550, spanning about 650–850 °C. Subalkaline granites at I.A about 550–650, up to about 870 °C."},
    {"name": "Mantle-derived granites",
     "text": "High I.A: {101}-dominated pyramids, the P, J and D types. Alkaline granites at I.A about 650–720 over about 550–890 °C. Tholeiitic granites at I.A about 700 and about 900 °C."},
    {"name": "Special markers",
     "text": "Charnockites (Ch) plot at about 850–875 °C and I.A about 300–450. The muscovite-granite limit (Mu) lies near I.T 450, about 725 °C. Field positions are read from redrawn figures and are good to about ±50 index units."},
]

REFERENCES = [
    ref("Pupin, J.P. (1980). Zircon and granite petrology. <i>Contributions to Mineralogy and Petrology</i> 73, 207–220.",
        "10.1007/BF00381441", "The typology reproduced in this matrix, with the I.A/I.T indices, 64 subtypes and petrogenetic fields.", ["typology"]),
    ref("Pupin, J.P., Turco, G. (1972). Une typologie originale du zircon accessoire. <i>Bulletin de la Société française de Minéralogie et de Cristallographie</i> 95, 348–359.",
        "10.3406/bulmi.1972.6688", "The original (French) version of the typology chart.", ["typology"]),
    ref("Pupin, J.P., Bonin, B., Tessier, M., Turco, G. (1978). Rôle de l'eau sur les caractères morphologiques et la cristallisation du zircon dans les granitoïdes. <i>Bulletin de la Société Géologique de France</i> S7-XX(5), 721–725.",
        "10.2113/gssgfbull.S7-XX.5.721", "Melt water content as an additional control on zircon habit.", ["typology"]),
    ref("Pupin, J.P., Turco, G. (1976). Occurrence of peculiar tabular zircon crystals. <i>Mineralogical Magazine</i> 40, 790–792.",
        "10.1180/minmag.1976.040.315.16", "Rare {001}-bearing tabular habit, which lies outside the 64-cell grid.", ["morphology"]),
    ref("Vavra, G. (1990). On the kinematics of zircon growth and its petrogenetic significance: a cathodoluminescence study. <i>Contributions to Mineralogy and Petrology</i> 106, 90–99.",
        "10.1007/BF00306410", "Growth-sector kinematics from CL. Habit changes during growth and is not a single equilibrium state.", ["morphology"]),
    ref("Vavra, G. (1993). A guide to quantitative morphology of accessory zircon. <i>Chemical Geology</i> 110, 15–28.",
        "10.1016/0009-2541(93)90245-E", "Quantitative morphology from relative face growth rates, the closest published analogue to the central-distance approach used here.", ["morphology", "method"]),
    ref("Vavra, G. (1994). Systematics of internal zircon morphology in major Variscan granitoid types. <i>Contributions to Mineralogy and Petrology</i> 117, 331–344.",
        "10.1007/BF00307269", "Internal (growth-zone) morphology by granite type.", ["morphology"]),
    ref("Benisek, A., Finger, F. (1993). Factors controlling the development of prism faces in granite zircons: a microprobe study. <i>Contributions to Mineralogy and Petrology</i> 114, 441–451.",
        "10.1007/BF00321749", "The main critique of the I.T thermometer: trace elements (U, Th, Y) taken up on prism faces affect {100}/{110} development.", ["critique"]),
    ref("Belousova, E.A., Griffin, W.L., O'Reilly, S.Y. (2006). Zircon crystal morphology, trace element signatures and Hf isotope composition as a tool for petrogenetic modelling: examples from Eastern Australian granitoids. <i>Journal of Petrology</i> 47, 329–353.",
        "10.1093/petrology/egi077", "Pupin-type morphology combined with trace elements and Hf isotopes.", ["typology"]),
    ref("Vavra, G., Schmid, R., Gebauer, D. (1999). Internal morphology, habit and U-Th-Pb microanalysis of amphibolite-to-granulite facies zircons: geochronology of the Ivrea Zone. <i>Contributions to Mineralogy and Petrology</i> 134, 380–404.",
        "10.1007/s004100050492", "Metamorphic zircon habits (equant, multifaceted) that fall outside the igneous typology.", ["morphology"]),
    ref("Corfu, F., Hanchar, J.M., Hoskin, P.W.O., Kinny, P. (2003). Atlas of zircon textures. <i>Reviews in Mineralogy and Geochemistry</i> 53, 469–500.",
        "10.2113/0530469", "The standard imaging reference for zircon habit and internal textures.", ["review"]),
    ref("Watson, E.B., Harrison, T.M. (1983). Zircon saturation revisited: temperature and composition effects in a variety of crustal magma types. <i>Earth and Planetary Science Letters</i> 64, 295–304.",
        "10.1016/0012-821X(83)90211-X", "The independent zircon-saturation temperature, often compared with Pupin's I.T.", ["thermometry"]),
    ref("Hourigan, J.K., Reiners, P.W., Brandon, M.T. (2005). U-Th zonation-dependent alpha-ejection in (U-Th)/He chronometry. <i>Geochimica et Cosmochimica Acta</i> 69, 3349–3365.",
        "10.1016/j.gca.2005.01.024", "F<sub>T</sub> corrections for tetragonal prisms with pyramidal terminations, the geometry modelled here.", ["thermochronology", "geometry"]),
    ref("Zeigler, S.D., Baker, M., Metcalf, J.R., Flowers, R.M. (2024). The Geometric Correction Method for zircon (U–Th)/He chronology. <i>Geochronology</i> 6, 199–226.",
        "10.5194/gchron-6-199-2024", "Compares 2D measurements with 3D nano-CT on 223 zircons. 2D geometry overestimates volume and F<sub>T</sub>.", ["thermochronology", "geometry"]),
    ref("Osorio-Granada, E., Restrepo-Moreno, S.A., Muñoz-Valencia, J.A., Trejos-Tamayo, R.A., Pardo-Trujillo, A., Barbosa-Espitia, A.A. (2017). Detrital zircon typology and U/Pb geochronology for the Miocene Ladrilleros-Juanchaco sedimentary sequence, Equatorial Pacific (Colombia). <i>Geologica Acta</i> 15(3), 201–215.",
        "10.1344/GeologicaActa2017.15.3.4", "Fig. 4 is an English-labelled reproduction of Pupin's chart, used here for the grid layout.", ["layout source"]),
    ref("Daneshvar, N., Maanijou, M., Azizi, H., Asahara, Y. (2018). Study of the zircon morphology and internal structures as a tool for constraining magma source: example from granitoid bodies in the northern Sanandaj Sirjan zone (SW Saqqez). <i>Geopersia</i> 8(2), 245–259.",
        "10.22059/GEOPE.2018.239656.648342", "Figs. 5–6 reproduce the original French chart and the petrogenetic fields, used here for the grid layout.", ["layout source"]),
    ref("Robinson, K., Gibbs, G.V., Ribbe, P.H. (1971). The structure of zircon: a comparison with garnet. <i>American Mineralogist</i> 56, 782–790.",
        None, "The source of the zircon cell used here (a = 6.607, c = 5.982 Å).", ["lattice"], url="http://www.minsocam.org/ammin/AM56/AM56_782.pdf"),
]
