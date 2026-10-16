"""Epidote (P2₁/m, b-unique; Dana/Koksharov indices = structural, no conversion)."""

from ._common import ref
from ._grid import form, grid_spec

ID = "epidote"
N = None

FORMS = [
    form("001", (0, 0, 1), "c, basal pinacoid (cleavage)", "#5f7a2a"),
    form("100", (1, 0, 0), "a, front pinacoid", "#7f9a3a"),
    form("-101", (-1, 0, 1), "r, hemidome", "#a5b94a"),
    form("101", (1, 0, 1), "e, hemidome", "#c4cf6e"),
    form("-111", (-1, 1, 1), "n, hemipyramid (termination)", "#d8c24a"),
    form("011", (0, 1, 1), "o, clinodome", "#b49a34"),
]
ROWS = [
    {"code": "1", "label": "L1", "detail": "1.5:1", "text": "short-prismatic along b, 1.5:1", "ops": [{"aspect": 1.5}]},
    {"code": "2", "label": "L2", "detail": "3:1", "text": "prismatic along b, 3:1", "ops": [{"aspect": 3.0}]},
    {"code": "3", "label": "L3", "detail": "6:1", "text": "long-prismatic along b, 6:1", "ops": [{"aspect": 6.0}]},
    {"code": "4", "label": "L4", "detail": "10:1", "text": "acicular along b, 10:1", "ops": [{"aspect": 10.0}]},
]
COLS = [
    {"code": "c", "label": "c", "detail": "(001)-flattened", "text": "prism zone flattened on (001)", "ops": [{"set": {"001": 0.6}}]},
    {"code": "b", "label": "b", "detail": "balanced c, a, r", "text": "balanced prism zone c{001}, a{100}, r{1̄01}", "ops": []},
    {"code": "a", "label": "a", "detail": "(100)-flattened", "text": "prism zone flattened on (100)", "ops": [{"set": {"100": 0.6}}]},
    {"code": "r", "label": "r", "detail": "r{1̄01} dominant", "text": "r{1̄01} dominant", "ops": [{"set": {"-101": 0.7}}]},
]


def spec():
    return grid_spec(
        id=ID, name="Epidote", formula="Ca₂Al₂Fe³⁺(Si₂O₇)(SiO₄)O(OH)", group="Sorosilicates",
        chronometers="U–Pb (hydrothermal veins); Sr, Pb isotopes",
        system="Monoclinic", setting="P2₁/m, b-unique (Dana's indices apply unchanged)",
        lattice=dict(a=8.8877, b=5.6275, c=10.1517, beta=115.383), lattice_source="Gabe et al. (1973)", point_group="2/m",
        forms=FORMS, base={"001": 0.9, "100": 0.9, "-101": 0.9, "101": 1.0, "-111": 1.0, "011": 1.05},
        rows=ROWS, cols=COLS, elongation_axis=(0, 1, 0), default=(1, 1), mono_color="#6f8a2a", view={"tilt": 14, "turn": -55},
        title="Prism zone × elongation along b",
        subtitle="Epidote is elongated along b, with a striated prism zone of c{001}, a{100}, r{1̄01} and e{101}, terminated by n{1̄11} and o{011}.",
        row_title="Aspect along b", col_title="Prism-zone section",
        note=("Nine interfacial angles match Dana (1892) to within 0.2°. No quantitative study links habit to conditions, so "
              "the levels describe the range of documented habits. Epidote is a sorosilicate (mixed SiO₄ and Si₂O₇ groups)."),
        about="""
<p>Epidote crystals are elongated along the b axis, the 2-fold axis, with a deeply striated prism zone of {h0l} faces. They are
usually terminated at only one end by n{1̄11}. Simple n- or o-terminated crystals look deceptively orthorhombic.
Epidote can now be dated directly by in-situ U–Pb to time hydrothermal veining (Peverelli et al. 2021).</p>""",
        habits=[
            {"name": "Prismatic along b", "text": "A striated c–a–r prism zone with a wedge termination by n{1̄11} (row L2)."},
            {"name": "Pseudo-orthorhombic", "text": "Terminated by n or o alone, which gives a deceptively orthorhombic look."},
            {"name": "Acicular / fibrous", "text": "Needles along b (row L4)."},
        ],
        references=[
            ref("Franz, G., Liebscher, A. (2004). Physical and chemical properties of the epidote minerals – an introduction. <i>Reviews in Mineralogy and Geochemistry</i> 56, 1–81.",
                "10.2138/gsrmg.56.1.1", "Crystallography, settings and morphology of the epidote group.", ["review"]),
            ref("Peverelli, V., Ewing, T., Rubatto, D., Wille, M., Berger, A., Villa, I.M., Lanari, P., Pettke, T., Herwegh, M. (2021). U–Pb geochronology of epidote by LA-ICP-MS as a tool for dating hydrothermal-vein formation. <i>Geochronology</i> 3, 123–147.",
                "10.5194/gchron-3-123-2021", "Direct epidote U–Pb dating.", ["geochronology"]),
            ref("Gabe, E.J., Portheine, J.C., Whitlow, S.H. (1973). A reinvestigation of the epidote structure: confirmation of the iron location. <i>American Mineralogist</i> 58, 218–223.",
                None, "The cell used here.", ["lattice"], url="http://www.minsocam.org/ammin/AM58/AM58_218.pdf"),
        ],
    )
