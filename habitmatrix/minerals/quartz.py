"""α-Quartz, point group 32 ('321': 2-folds along the a axes); Dana's axes = structural, no conversion."""

from ._common import ref
from ._grid import form, grid_spec

ID = "quartz"
N = None

FORMS = [
    form("10-10", (1, 0, -1, 0), "m, hexagonal prism", "#c9d6e3"),
    form("10-11", (1, 0, -1, 1), "r, major rhombohedron", "#8fa8c8"),
    form("01-11", (0, 1, -1, 1), "z, minor rhombohedron", "#b7c7dd"),
    form("11-21", (1, 1, -2, 1), "s, trigonal bipyramid (right-handed)", "#e3c27a"),
    form("51-61", (5, 1, -6, 1), "x, trigonal trapezohedron (right-handed)", "#d99a6c"),
]
ROWS = [
    {"code": "B", "label": "B", "detail": "no prism", "text": "bipyramidal, no prism (β-quartz paramorph habit)", "ops": [{"set": {"10-10": N}}]},
    {"code": "1", "label": "P1", "detail": "stubby", "text": "stubby prism, d(m)/d(r) = 1.0", "ops": [{"set": {"10-10": 1.0}}]},
    {"code": "2", "label": "P2", "detail": "prismatic", "text": "prismatic, d(m)/d(r) = 0.6", "ops": [{"set": {"10-10": 0.6}}]},
    {"code": "3", "label": "P3", "detail": "elongate", "text": "elongate, d(m)/d(r) = 0.4", "ops": [{"set": {"10-10": 0.4}}]},
    {"code": "4", "label": "P4", "detail": "needle", "text": "needle-like, d(m)/d(r) = 0.25", "ops": [{"set": {"10-10": 0.25}}]},
]
COLS = [
    {"code": "a", "label": "a", "detail": "r = z", "text": "r = z, pseudo-hexagonal pyramid", "ops": [{"set": {"01-11": 1.0}}]},
    {"code": "b", "label": "b", "detail": "r > z (typical)", "text": "r slightly larger than z (typical)", "ops": [{"set": {"01-11": 1.08}}]},
    {"code": "c", "label": "c", "detail": "z small", "text": "z small", "ops": [{"set": {"01-11": 1.15}}]},
    {"code": "d", "label": "d", "detail": "r only", "text": "r only (pseudocubic rhombohedron without a prism)", "ops": [{"set": {"01-11": N}}]},
    {"code": "R", "label": "R", "detail": "right-handed s + x", "text": "right-handed crystal with s{112̄1} and x{516̄1}",
     "ops": [{"set": {"01-11": 1.1}}, {"share": ["11-21", 0.06, "10-11"], "stage": 0.6},
             {"share": ["51-61", 0.08, "10-11"], "requires": "10-10", "stage": 0.7}]},
]


def spec():
    return grid_spec(
        id=ID, name="Quartz", formula="SiO₂", group="Framework silicates",
        chronometers="Ti-in-quartz thermometry; OSL/ESR dating; cosmogenic nuclides",
        system="Trigonal", setting="P3₂21 / P3₁21, hexagonal axes (point group 32)",
        lattice=dict(a=4.913437, b=4.913437, c=5.405118, gamma=120), lattice_source="Antao et al. (2008)", point_group="32",
        forms=FORMS, base={"10-11": 1.0},
        rows=ROWS, cols=COLS, default=(2, 1), mono_color="#cdd6e0", view={"tilt": 12, "turn": -18},
        title="Prism length × rhombohedron balance",
        subtitle="Rows lengthen the m{101̄0} prism, from the bipyramid of volcanic quartz to needles. Columns balance the two rhombohedra r and z, and the last column adds the trigonal faces s and x that reveal a right-handed crystal.",
        row_title="Prism development", col_title="Termination",
        note=("Eight interfacial angles match Dana (1892) to within 0.02°, for example m∧r = 38.22° against 38°13′. Point group 32 "
              "has no mirrors or inversion, so r and z are different forms, s is a trigonal bipyramid and x a trigonal "
              "trapezohedron. Handedness follows Dana's morphological convention; the link to the P3₁21 or P3₂21 label is "
              "notoriously confusing (Donnay &amp; Le Page 1978), so no space-group label is attached to the right-handed "
              "crystals. On real crystals r and z are told apart by etching; here r is simply the larger rhombohedron. "
              "Dauphiné and Brazil twins and tapering 'Tessin' habits are not modelled."),
        about="""
<p>Quartz looks hexagonal but is trigonal, with point group 32. The six terminal faces are really two different
rhombohedra, r and z. They are often unequal, so alternate termination faces differ in size. The small s and x faces
appear only on one side of each prism face and reveal whether a crystal is left- or right-handed.</p>
<p>Habit tracks conditions. Quartz phenocrysts in rhyolites and porphyries are prismless bipyramids, often paramorphs
after high-temperature β-quartz (Hosaka et al. 1995). Vein and Alpine-fissure quartz is prismatic with sector-zoned r, z
and m faces (Jourdan et al. 2009). Ti-in-quartz thermometry (TitaniQ) can depend on which growth sector a spot hits.</p>""",
        habits=[
            {"name": "Prismatic", "text": "m prism with r and z terminations, r usually larger (row P2, column b)."},
            {"name": "Bipyramidal", "text": "No prism, r ≈ z: volcanic quartz grown as β-quartz (row B)."},
            {"name": "Pseudocubic", "text": "r alone forms a near-cubic rhombohedron, r∧r′ = 85°46′ (row B, column d)."},
            {"name": "Right-handed", "text": "Small s and x faces at alternate corners of the prism (column R)."},
        ],
        references=[
            ref("Antao, S.M., Hassan, I., Wang, J., Lee, P.L., Toby, B.H. (2008). State-of-the-art high-resolution powder X-ray diffraction (HRPXRD) illustrated with Rietveld structure refinement of quartz, sodalite, tremolite, and meionite. <i>The Canadian Mineralogist</i> 46, 1501–1509.",
                "10.3749/canmin.46.5.1501", "The cell used here.", ["lattice"]),
            ref("Donnay, J.D.H., Le Page, Y. (1978). The vicissitudes of the low-quartz crystal setting or the pitfalls of enantiomorphism. <i>Acta Crystallographica A</i> 34, 584–594.",
                "10.1107/S0567739478001242", "The definitive account of r/z, handedness and the structural setting.", ["crystallography"]),
            ref("Le Page, Y., Donnay, G. (1976). Refinement of the crystal structure of low-quartz. <i>Acta Crystallographica B</i> 32, 2456–2459.",
                "10.1107/S0567740876007966", "Classic structure refinement.", ["lattice"]),
            ref("Hosaka, M., Miyata, T., Sunagawa, I. (1995). Growth and morphology of quartz crystals synthesized above the transition temperature. <i>Journal of Crystal Growth</i> 152, 300–306.",
                "10.1016/0022-0248(95)00139-5", "Morphology of quartz grown as β-quartz, behind the bipyramidal habit.", ["morphology"]),
            ref("Jourdan, A.-L., Mullis, J., Ramseyer, K., Spiers, C.J. (2009). Evidence of growth and sector zoning in hydrothermal quartz from Alpine veins. <i>European Journal of Mineralogy</i> 21, 219–231.",
                "10.1127/0935-1221/2009/0021-1881", "Growth and sector zoning on r, z and m in vein quartz.", ["morphology"]),
            ref("Wark, D.A., Watson, E.B. (2006). TitaniQ: a titanium-in-quartz geothermometer. <i>Contributions to Mineralogy and Petrology</i> 152, 743–754.",
                "10.1007/s00410-006-0132-1", "Quartz thermometry.", ["thermometry"]),
            ref("Thomas, J.B., Watson, E.B., Spear, F.S., Shemella, P.T., Nayak, S.K., Lanzirotti, A. (2010). TitaniQ under pressure: the effect of pressure and temperature on the solubility of Ti in quartz. <i>Contributions to Mineralogy and Petrology</i> 160, 743–759.",
                "10.1007/s00410-010-0505-3", "Pressure-dependent recalibration of TitaniQ.", ["thermometry"]),
            ref("Morgan, D.J., Jerram, D.A. (2006). On estimating crystal shape for crystal size distribution analysis. <i>Journal of Volcanology and Geothermal Research</i> 154, 1–7.",
                "10.1016/j.jvolgeores.2005.09.016", "Estimating 3D crystal shape from 2D sections for CSD work.", ["geometry"]),
        ],
    )
