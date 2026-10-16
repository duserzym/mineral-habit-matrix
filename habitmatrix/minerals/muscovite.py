"""Muscovite-2M₁ (C2/c).  Dana/Tschermak pseudo-orthohexagonal indices mapped numerically:
M(221) -> (110), μ(-111) -> (-111), x(-131) -> (-131)."""

from ._common import ref
from ._grid import form, grid_spec

ID = "muscovite"
N = None

FORMS = [
    form("001", (0, 0, 1), "c, basal pinacoid (cleavage)", "#c9c3a8"),
    form("110", (1, 1, 0), "M, prism", "#9c9478"),
    form("010", (0, 1, 0), "b, side pinacoid", "#b3ab8c"),
    form("-111", (-1, 1, 1), "μ, steep hemipyramid", "#7e7860"),
    form("-131", (-1, 3, 1), "x, hemipyramid", "#e2dcc2"),
]
ROWS = [
    {"code": "1", "label": "T1", "detail": "1:20 flake", "text": "thin flake, thickness:diameter 1:20", "ops": [{"aspect": 0.05}]},
    {"code": "2", "label": "T2", "detail": "1:8", "text": "plate, 1:8", "ops": [{"aspect": 0.125}]},
    {"code": "3", "label": "T3", "detail": "1:3", "text": "thick plate, 1:3", "ops": [{"aspect": 0.33}]},
    {"code": "4", "label": "T4", "detail": "1:1 book", "text": "book, 1:1", "ops": [{"aspect": 1.0}]},
]
COLS = [
    {"code": "r", "label": "r", "detail": "rhombic {110}", "text": "rhombic (diamond) outline of {110}", "ops": [{"set": {"010": N, "-111": N, "-131": N}}]},
    {"code": "h", "label": "h", "detail": "hexagon {110}+{010}", "text": "pseudo-hexagonal {110}+{010}", "ops": [{"set": {"-111": N, "-131": N}}]},
    {"code": "μ", "label": "μ", "detail": "+ {1̄11}", "text": "pseudo-hexagonal with steep {1̄11}", "ops": [{"set": {"-131": N, "-111": 0.95}}]},
    {"code": "t", "label": "t", "detail": "tapering", "text": "tapering, with larger {1̄11} and {1̄31}", "ops": [{"set": {"-111": 0.92, "-131": 0.98}}]},
]


def spec():
    return grid_spec(
        id=ID, name="Muscovite", formula="KAl₂(AlSi₃O₁₀)(OH)₂", group="Sheet silicates",
        chronometers="⁴⁰Ar/³⁹Ar, K–Ar, Rb–Sr",
        system="Monoclinic", setting="C2/c, 2M₁ polytype",
        lattice=dict(a=5.189, b=8.996, c=20.096, beta=95.18), lattice_source="Radoslovich (1960)", point_group="2/m",
        forms=FORMS, base={"001": 0.02, "110": 1.0, "010": 1.0, "-111": 1.0, "-131": 1.05},
        rows=ROWS, cols=COLS, elongation_axis=(0, 0, 1), measure_plane=(0, 0, 1), default=(1, 1),
        mono_color="#bdb69a", view={"tilt": 38, "turn": -20},
        title="Plate outline × thickness",
        subtitle="Basal {001} plates bounded by {110} and {010}, with the steep hemipyramids {1̄11} and {1̄31} that make tapering 'barrel' books.",
        row_title="Thickness : diameter", col_title="Outline / lateral forms",
        note=("Dana's pseudo-orthohexagonal indices were mapped numerically to the 2M₁ cell: M(221) → (110), μ(1̄11) → (1̄11), "
              "x(1̄31) → (1̄31). Nine angles match Dana to within 0.2°, for example (110)∧(11̄0) = 59.75° against 59°48′. "
              "Real lateral faces are rough and vicinal, and twins are common."),
        about="""
<p>Muscovite's 2M₁ cell gives a genuinely monoclinic plate: the {110} prism and {1̄11} hemipyramid are steep (85.5° and
81.7° from (001)) rather than exactly vertical. That is why thick books taper. For <sup>40</sup>Ar/<sup>39</sup>Ar
thermochronology the plate radius is roughly the diffusion domain (Hames &amp; Bowring 1994), so the outline and
thickness here relate directly to closure temperature. Compare the biotite page, which uses an idealized
orthohexagonal cell.</p>""",
        habits=[
            {"name": "Pseudo-hexagonal plate", "text": "Tabular on (001), with 60°/120° plane angles (column h)."},
            {"name": "Rhombic plate", "text": "c + {110} only (column r)."},
            {"name": "Tapering book", "text": "Thick crystals whose sides converge through steep {110}/{1̄11} faces (column t, row T4)."},
        ],
        references=[
            ref("Radoslovich, E.W. (1960). The structure of muscovite, KAl<sub>2</sub>(Si<sub>3</sub>Al)O<sub>10</sub>(OH)<sub>2</sub>. <i>Acta Crystallographica</i> 13, 919–932.",
                "10.1107/S0365110X60002259", "The 2M₁ cell used here.", ["lattice"]),
            ref("Hames, W.E., Bowring, S.A. (1994). An empirical evaluation of the argon diffusion geometry in muscovite. <i>Earth and Planetary Science Letters</i> 124, 161–169.",
                "10.1016/0012-821X(94)00079-4", "Grain size and shape as the Ar diffusion domain.", ["thermochronology", "geometry"]),
            ref("Harrison, T.M., Célérier, J., Aikman, A.B., Hermann, J., Heizler, M.T. (2009). Diffusion of <sup>40</sup>Ar in muscovite. <i>Geochimica et Cosmochimica Acta</i> 73, 1039–1051.",
                "10.1016/j.gca.2008.09.038", "Ar diffusion parameters using cylindrical geometry.", ["thermochronology"]),
        ],
    )
