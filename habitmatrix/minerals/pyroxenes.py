"""Orthopyroxene (Pbca) and clinopyroxene (C2/c) habit matrices."""

from ._common import ref
from ._grid import form, grid_spec

N = None
ASPECT_ROWS = [
    {"code": "1", "label": "L1", "detail": "stubby 1.3:1", "text": "stubby, 1.3:1", "ops": [{"aspect": 1.3}]},
    {"code": "2", "label": "L2", "detail": "2:1", "text": "prismatic, 2:1", "ops": [{"aspect": 2.0}]},
    {"code": "4", "label": "L4", "detail": "4:1", "text": "long-prismatic, 4:1", "ops": [{"aspect": 4.0}]},
    {"code": "8", "label": "L8", "detail": "8:1", "text": "acicular, 8:1", "ops": [{"aspect": 8.0}]},
]


def opx_spec():
    forms = [
        form("210", (2, 1, 0), "m, prism (88° cleavage)", "#5a6b3a"),
        form("100", (1, 0, 0), "a, front pinacoid", "#8a8a52"),
        form("010", (0, 1, 0), "b, side pinacoid", "#a9a46a"),
        form("211", (2, 1, 1), "o, dipyramid", "#c9b27a"),
        form("111", (1, 1, 1), "e, dipyramid", "#e1d3a2"),
    ]
    cols = [
        {"code": "s", "label": "s", "detail": "square {100}+{010}", "text": "square section {100}+{010}", "ops": [{"set": {"210": N, "100": 0.95, "010": 0.95}}]},
        {"code": "o", "label": "o", "detail": "octagonal", "text": "octagonal section {100}+{010}+{210}", "ops": [{"set": {"100": 0.9, "010": 0.9}}]},
        {"code": "m", "label": "m", "detail": "{210} rhomb (88°)", "text": "{210} rhombic section (88°)", "ops": [{"set": {"100": N, "010": N}}]},
        {"code": "b", "label": "b", "detail": "tabular (010)", "text": "tabular on (010)", "ops": [{"set": {"010": 0.55, "100": 0.95}}]},
        {"code": "a", "label": "a", "detail": "tabular (100)", "text": "tabular on (100)", "ops": [{"set": {"100": 0.55, "010": 0.95}}]},
    ]
    return grid_spec(
        id="orthopyroxene", name="Orthopyroxene", formula="(Mg,Fe)₂Si₂O₆", group="Chain silicates",
        chronometers="Fe–Mg diffusion chronometry; two-pyroxene thermometry",
        system="Orthorhombic", setting="Pbca (structural, a doubled; Dana (hkl) → (2k, h, l))",
        lattice=dict(a=18.2588, b=8.8229, c=5.1899), lattice_source="Nestola et al. (2006)", point_group="mmm",
        forms=forms, base={"210": 1.0, "100": 0.9, "010": 0.9, "211": 1.1, "111": 1.15},
        rows=ASPECT_ROWS, cols=cols, default=(1, 1), mono_color="#5d6a3e", view={"tilt": 14, "turn": -30},
        title="Prism cross-section × elongation",
        subtitle="Prismatic along [001], terminated by the dipyramids {211} and {111}. Columns change the cross-section from square to octagonal, rhombic and tabular.",
        row_title="Aspect (L/W)", col_title="Cross-section",
        note=("Indices are structural Pbca. Dana's morphological axes have a<sub>D</sub> = b, b<sub>D</sub> = a/2, so Dana's "
              "(hkl) is (2k, h, l) here, and his letters a and b point at structural (010) and (100). Eight interfacial "
              "angles match Dana to within 0.25°. Which terminations dominate is poorly documented."),
        about="""
<p>Orthopyroxene phenocrysts are prismatic along [001] with a characteristic eight-sided basal section built from
{100}, {010} and the {210} cleavage prism, whose faces meet at about 88°. Hypersthene is often tabular on (010).
Orthopyroxene is used for Fe–Mg <strong>diffusion chronometry</strong> of magma storage and ascent (Allan et al. 2013;
Dohmen et al. 2016). Its 3D shape controls how a thin section samples the zoning.</p>""",
        habits=[
            {"name": "Octagonal prism", "text": "{100} + {010} + {210}, the standard basal section of volcanic orthopyroxene (column o)."},
            {"name": "Tabular on (010)", "text": "Dana: hypersthene is often tabular parallel to (010) in the structural cell (column b)."},
            {"name": "Acicular", "text": "Rosettes of needles along [001] from fast growth (row L8)."},
        ],
        references=[
            ref("Nestola, F., Gatta, G.D., Boffa Ballaran, T. (2006). The effect of Ca substitution on the elastic and structural behavior of orthoenstatite. <i>American Mineralogist</i> 91, 809–815.",
                "10.2138/am.2006.1982", "The Pbca cell used here.", ["lattice"]),
            ref("Dohmen, R., ter Heege, J.H., Becker, H.-W., Chakraborty, S. (2016). Fe-Mg interdiffusion in orthopyroxene. <i>American Mineralogist</i> 101, 2210–2221.",
                "10.2138/am-2016-5815", "Diffusion data for orthopyroxene chronometry.", ["diffusion"]),
            ref("Allan, A.S.R., Morgan, D.J., Wilson, C.J.N., Millet, M.-A. (2013). From mush to eruption in centuries: assembly of the super-sized Oruanui magma body. <i>Contributions to Mineralogy and Petrology</i> 166, 143–164.",
                "10.1007/s00410-013-0869-2", "Applied orthopyroxene Fe–Mg diffusion chronometry.", ["chronometry"]),
        ],
    )


def cpx_spec():
    forms = [
        form("100", (1, 0, 0), "a, front pinacoid", "#3f5b3a"),
        form("010", (0, 1, 0), "b, side pinacoid", "#5f7d4a"),
        form("110", (1, 1, 0), "m, prism (87°/93° cleavage)", "#22382a"),
        form("-111", (-1, 1, 1), "s, hemipyramid (augite termination)", "#8fa36a"),
        form("001", (0, 0, 1), "c, basal pinacoid", "#b9b98a"),
        form("-101", (-1, 0, 1), "p, hemidome", "#a3b48a"),
    ]
    cols = [
        {"code": "s", "label": "s", "detail": "square {100}+{010}", "text": "square section {100}+{010}", "ops": [{"set": {"110": N, "100": 0.95, "010": 0.95}}]},
        {"code": "o", "label": "o", "detail": "octagonal (augite)", "text": "octagonal augite section {100}+{010}+{110}", "ops": [{"set": {"100": 0.86, "010": 0.86}}]},
        {"code": "m", "label": "m", "detail": "{110} dominant", "text": "{110}-dominated near-square rhomb", "ops": [{"set": {"100": 0.98, "010": 0.98}}]},
        {"code": "d", "label": "d", "detail": "diopside ends", "text": "octagonal, with {001} and {1̄01} diopside terminations", "ops": [{"set": {"100": 0.86, "010": 0.86, "001": 1.18, "-101": 1.12}}]},
    ]
    return grid_spec(
        id="clinopyroxene", name="Clinopyroxene", formula="Ca(Mg,Fe)Si₂O₆ (diopside–augite)", group="Chain silicates",
        chronometers="Fe–Mg diffusion chronometry; sector-zoning records of ascent",
        system="Monoclinic", setting="C2/c, obtuse β (Dana's indices apply unchanged)",
        lattice=dict(a=9.7397, b=8.9174, c=5.2503, beta=105.866), lattice_source="Thompson &amp; Downs (2008), diopside", point_group="2/m",
        forms=forms, base={"100": 0.86, "010": 0.86, "110": 1.0, "-111": 1.12, "001": N, "-101": N},
        rows=ASPECT_ROWS, cols=cols, default=(0, 1), mono_color="#2f4a35", view={"tilt": 14, "turn": -30},
        title="Prism cross-section × elongation",
        subtitle="Short-prismatic along [001] with the roof-like {1̄11} augite termination. The last column adds the {001} and {1̄01} diopside terminations.",
        row_title="Aspect (L/W)", col_title="Cross-section",
        note=("Dana's β = 74°10′ is the interfacial angle (001)∧(100), so his indices equal the modern obtuse-β C2/c indices "
              "with no sign flip. (001)∧(101) = 24.32° here against Dana's 24°21′. The cell is diopside's; augite's β is "
              "about 1° larger. The (100) contact twin and skeletal quench crystals are not modelled."),
        about="""
<p>Augite is classically a stubby, nearly symmetric eight-sided prism of {100}, {010} and {110}, terminated by the
hemipyramid {1̄11}. Diopside is longer-prismatic with {001} and {1̄01} ends. The faces of the crystal set its growth
sectors. Sector-zoned augite, with {1̄11} "hourglass" sectors against the prism sectors, records undercooling and ascent
rate (Kouchi et al. 1983; Ubide et al. 2019). Zoned clinopyroxene is also a time capsule of eruption history (Ubide &amp;
Kamber 2018).</p>""",
        habits=[
            {"name": "Augite, octagonal", "text": "A nearly symmetric 8-sided prism of a, b and m with a roof-like {1̄11} termination (column o, row L1)."},
            {"name": "Square prism", "text": "Dana: a square prism with a and b prominent (column s)."},
            {"name": "{110}-dominated", "text": "A near-square rhomb of the 87°/93° cleavage prism (column m)."},
            {"name": "Diopside", "text": "Prismatic, with {001}, {1̄01} and {1̄11} terminations (column d)."},
        ],
        references=[
            ref("Thompson, R.M., Downs, R.T. (2008). The crystal structure of diopside at pressure to 10 GPa. <i>American Mineralogist</i> 93, 177–186.",
                "10.2138/am.2008.2684", "The C2/c cell used here.", ["lattice"]),
            ref("Kouchi, A., Sugawara, Y., Kashima, K., Sunagawa, I. (1983). Laboratory growth of sector zoned clinopyroxenes in the system CaMgSi<sub>2</sub>O<sub>6</sub>–CaTiAl<sub>2</sub>O<sub>6</sub>. <i>Contributions to Mineralogy and Petrology</i> 83, 177–184.",
                "10.1007/BF00373091", "Experimental growth of sector zoning versus supersaturation.", ["morphology"]),
            ref("Ubide, T., Mollo, S., Zhao, J.-x., Nazzari, M., Scarlato, P. (2019). Sector-zoned clinopyroxene as a recorder of magma history, eruption triggers, and ascent rates. <i>Geochimica et Cosmochimica Acta</i> 251, 265–283.",
                "10.1016/j.gca.2019.02.021", "{1̄11} hourglass sectors versus prism sectors: growth kinetics of individual faces.", ["morphology", "chronometry"]),
            ref("Ubide, T., Kamber, B.S. (2018). Volcanic crystals as time capsules of eruption history. <i>Nature Communications</i> 9, 326.",
                "10.1038/s41467-017-02274-w", "Augite zoning as a record of eruption timing.", ["chronometry"]),
            ref("Shea, T., Hammer, J.E. (2013). Kinetics of cooling- and decompression-induced crystallization in hydrous mafic-intermediate magmas. <i>Journal of Volcanology and Geothermal Research</i> 260, 127–145.",
                "10.1016/j.jvolgeores.2013.04.018", "Crystal morphology versus undercooling in mafic magmas.", ["morphology"]),
            ref("Müller, T., Dohmen, R., Becker, H.-W., ter Heege, J.H., Chakraborty, S. (2013). Fe–Mg interdiffusion rates in clinopyroxene: experimental data and implications for Fe–Mg exchange geothermometers. <i>Contributions to Mineralogy and Petrology</i> 166, 1563–1576.",
                "10.1007/s00410-013-0941-y", "Diffusion data for clinopyroxene chronometry.", ["diffusion"]),
        ],
    )
