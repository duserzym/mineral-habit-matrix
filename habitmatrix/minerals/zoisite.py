"""Zoisite (Pnma; morphological (hkl) -> structural (k, l, h), Hurlbut 1969)."""

from ._common import ref
from ._grid import form, grid_spec

ID = "zoisite"
N = None

FORMS = [
    form("100", (1, 0, 0), "pinacoid (Dana b; cleavage)", "#7a7fa8"),
    form("001", (0, 0, 1), "pinacoid (Dana a)", "#9ba0c6"),
    form("101", (1, 0, 1), "m, prism ∥ b (Dana {110})", "#5b5f8a"),
    form("201", (2, 0, 1), "r, prism ∥ b (Dana {120})", "#b9bcdc"),
    form("011", (0, 1, 1), "d, dome (termination)", "#c9a6d6"),
    form("111", (1, 1, 1), "o, dipyramid (termination)", "#a481b8"),
]
ROWS = [
    {"code": "1", "label": "L1", "detail": "1.5:1", "text": "short-prismatic along b, 1.5:1", "ops": [{"aspect": 1.5}]},
    {"code": "2", "label": "L2", "detail": "3:1", "text": "prismatic along b, 3:1", "ops": [{"aspect": 3.0}]},
    {"code": "3", "label": "L3", "detail": "6:1", "text": "long-prismatic along b, 6:1", "ops": [{"aspect": 6.0}]},
]
COLS = [
    {"code": "s", "label": "s", "detail": "square (100)+(001)", "text": "squarish (100)+(001) section (tanzanite)", "ops": [{"set": {"101": 1.1, "201": N}}]},
    {"code": "m", "label": "m", "detail": "{101} rhombic", "text": "{101}-rhombic section", "ops": [{"set": {"100": 1.15, "001": 1.15, "101": 0.85}}]},
    {"code": "a", "label": "a", "detail": "(100)-flattened", "text": "flattened on (100)", "ops": [{"set": {"100": 0.55}}]},
]


def spec():
    return grid_spec(
        id=ID, name="Zoisite", formula="Ca₂Al₃(Si₂O₇)(SiO₄)O(OH)", group="Sorosilicates",
        chronometers="Sr–Pb isotopes; HP metamorphism (eclogite) petrology",
        system="Orthorhombic", setting="Pnma (morphological (hkl) → (k, l, h))",
        lattice=dict(a=16.1909, b=5.5466, c=10.0323), lattice_source="Smith et al. (1987), via Handbook of Mineralogy", point_group="mmm",
        forms=FORMS, base={"100": 0.95, "001": 0.95, "101": 1.0, "201": 1.05, "011": 1.0, "111": 1.05},
        rows=ROWS, cols=COLS, elongation_axis=(0, 1, 0), default=(1, 0), mono_color="#7b7fb0", view={"tilt": 14, "turn": -55},
        title="Prism zone × elongation along b",
        subtitle="Prismatic along b, deeply striated, with {011} and {111} terminations. Columns run from the squarish tanzanite section to {101}-rhombic and (100)-flattened sections.",
        row_title="Aspect along b", col_title="Prism-zone section",
        note=("The prism-zone indices are solid: eight interfacial angles match Dana (1892) to within 0.05°. The terminal "
              "forms are only moderately constrained, because natural crystals are seldom well terminated, so this matrix "
              "uses a generic {011} + {111} termination."),
        about="""
<p>Zoisite is the orthorhombic polymorph of clinozoisite. It is prismatic and deeply striated along b, and is a
characteristic mineral of high-pressure metamorphic rocks. Gem tanzanite crystals are often squarish in section with
equally developed (100) and (001) (Hurlbut 1969). Classical morphology uses a permuted cell, so Dana's letters a and b
point at structural (001) and (100).</p>""",
        habits=[
            {"name": "Metamorphic prismatic", "text": "Striated along b and poorly terminated, with {101} and (100) dominant."},
            {"name": "Tanzanite, squarish", "text": "(100) ≈ (001), well terminated (column s)."},
        ],
        references=[
            ref("Hurlbut, C.S. Jr. (1969). Gem zoisite from Tanzania. <i>American Mineralogist</i> 54, 702–709.",
                None, "Tanzanite morphology, habit types and the transform from morphological to X-ray axes.", ["morphology"], url="http://www.minsocam.org/ammin/AM54/AM54_702.pdf"),
            ref("Franz, G., Liebscher, A. (2004). Physical and chemical properties of the epidote minerals – an introduction. <i>Reviews in Mineralogy and Geochemistry</i> 56, 1–81.",
                "10.2138/gsrmg.56.1.1", "Zoisite crystallography and settings.", ["review"]),
            ref("Smith, J.V., Pluth, J.J., Richardson, J.W. Jr., Kvick, Å. (1987). Neutron diffraction study of zoisite at 15 K and X-ray study at room temperature. <i>Zeitschrift für Kristallographie</i> 179, 305–321.",
                "10.1524/zkri.1987.179.14.305", "Structure and the cell used here.", ["lattice"]),
            ref("Alvaro, M., Angel, R.J., Cámara, F. (2012). High-pressure behavior of zoisite. <i>American Mineralogist</i> 97, 1165–1176.",
                "10.2138/am.2012.4014", "Modern Pnma structure work.", ["lattice"]),
        ],
    )
