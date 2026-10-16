"""Carbonates, sulfates, halides, oxides and sulfides.

Structural-cell conversions from Dana (1892), each checked against Dana's interfacial angles:
  calcite, dolomite:  morph (h k i l) -> (h k i 4l)        (c_struct = 4 c_morph)
  ilmenite:           morph (h k i l) -> (h k i -2l)       (c doubled; obverse lattice)
  gypsum (A2/a):      ((h-l)/2, k, l)_Dana
  barite (Pnma):      (2h, k, l)_Dana
  anhydrite (Amma):   morph axes (a, b, c) = structural (c, a, b)
  aragonite, cubic minerals: no conversion
"""

from ._common import ref
from ._grid import form, grid_spec

N = None


def _rows(spec):
    return [{"code": c, "label": c, "detail": det, "text": txt, "ops": ops} for c, det, txt, ops in spec]


# ----------------------------------------------------------------- carbonates
SED_REFS = [
    ref("Folk, R.L. (1974). The natural history of crystalline calcium carbonate; effect of magnesium content and salinity. <i>Journal of Sedimentary Petrology</i> 44, 40–53.",
        "10.1306/74D72973-2B21-11D7-8648000102C1865D", "Classic model: Mg poisoning gives fibrous calcite elongated along c, versus equant meteoric calcite.", ["morphology"]),
    ref("Given, R.K., Wilkinson, B.H. (1985). Kinetic control of morphology, composition, and mineralogy of abiotic sedimentary carbonates. <i>Journal of Sedimentary Petrology</i> 55, 109–119.",
        "10.1306/212F862A-2B24-11D7-8648000102C1865D", "Equant versus acicular habit as a record of reactant supply rate.", ["morphology"]),
]


def calcite_spec():
    forms = [
        form("10-10", (1, 0, -1, 0), "m, hexagonal prism", "#e8e1cf"),
        form("0001", (0, 0, 0, 1), "c, basal pinacoid", "#b9ae94"),
        form("10-14", (1, 0, -1, 4), "r, cleavage rhombohedron", "#f3d9a7"),
        form("01-18", (0, 1, -1, 8), "e, flat rhombohedron", "#d9c08a"),
        form("10-11", (1, 0, -1, 1), "M, steep rhombohedron", "#c9a46a"),
        form("21-34", (2, 1, -3, 4), "v, scalenohedron (dogtooth)", "#e6b77a"),
    ]
    rows = _rows([
        ("T", "tabular", "tabular (paper spar), c{0001} at 0.3", [{"set": {"10-10": 1.0, "0001": 0.3}}]),
        ("Q", "no prism", "equant, no prism", []),
        ("P1", "short prism", "short prism, d(m) = 0.8", [{"set": {"10-10": 0.8}}]),
        ("P2", "prismatic", "prismatic, d(m) = 0.5", [{"set": {"10-10": 0.5}}]),
        ("P3", "acicular", "acicular / fibrous, d(m) = 0.3", [{"set": {"10-10": 0.3}}]),
    ])
    cols = [{"code": c, "label": lab, "detail": det, "text": f"terminated by {txt}", "ops": [{"set": {k: 1.0}}]}
            for c, lab, det, txt, k in [("e", "e", "flat rhombohedron", "the flat rhombohedron e{011̄8} (nailhead cap)", "01-18"),
                                        ("r", "r", "cleavage rhombohedron", "the cleavage rhombohedron r{101̄4}", "10-14"),
                                        ("M", "M", "steep rhombohedron", "the steep rhombohedron M{101̄1}", "10-11"),
                                        ("v", "v", "scalenohedron", "the scalenohedron v{213̄4} (dogtooth spar)", "21-34")]]
    return grid_spec(
        id="calcite", name="Calcite", formula="CaCO₃", group="Carbonates",
        chronometers="U–Pb carbonate dating; clumped isotopes; δ¹⁸O, δ¹³C",
        system="Trigonal", setting="R3̄c, obverse hexagonal axes (Dana (hkil) → (h k i 4l))",
        lattice=dict(a=4.991, b=4.991, c=17.062, gamma=120), lattice_source="Maslen et al. (1993)", point_group="-3m",
        forms=forms, base={}, rows=rows, cols=cols, default=(1, 1), mono_color="#efe6d2", view={"tilt": 16, "turn": -20},
        title="Prism length × termination",
        subtitle="Calcite's famous variety comes from a few forms: the cleavage rhombohedron r, the flat e (nailhead spar), the steep M, the scalenohedron v (dogtooth spar), the prism m and the pinacoid c. Columns run roughly from low to high supersaturation, and rows from tablets to fibres.",
        row_title="Prism development", col_title="Termination",
        note=("Dana's morphological cell has c one quarter of the structural c, so his cleavage rhombohedron (101̄1) is {101̄4} "
              "here and the scalenohedron v(213̄1) is {213̄4}. r∧r′ = 74.93° against Dana's 74°55′. The ordering of "
              "terminations by supersaturation follows the speleothem study of Gonzalez et al. (1992) and is qualitative."),
        about="""
<p>Calcite has more recorded crystal forms than almost any other mineral, but a handful explain most habits. In
speleothems, below about 6× supersaturation only rhombohedra grow; scalenohedra, steep rhombohedra, prism and
pinacoid appear at higher supersaturation (Gonzalez et al. 1992). Mg²⁺ adsorbed on the {101̄4} steps changes growth
(Davis et al. 2000) and favours fibrous, c-elongated marine calcite (Folk 1974), while reactant supply rate also
matters (Given &amp; Wilkinson 1985). Trace elements are incorporated step by step on the growth hillocks (Paquette
&amp; Reeder 1995). These are the same crystals now dated by LA-ICP-MS U–Pb (Roberts et al. 2020) and used for clumped-isotope
thermometry.</p>""",
        habits=[
            {"name": "Cleavage rhombohedron", "text": "r{101̄4} alone (row Q, column r)."},
            {"name": "Nailhead spar", "text": "Short prism capped by the flat rhombohedron e (row P1, column e)."},
            {"name": "Dogtooth spar", "text": "The scalenohedron v (column v)."},
            {"name": "Fibrous / columnar", "text": "Long m prisms (rows P2–P3)."},
            {"name": "Paper spar", "text": "Thin plates on c{0001} (row T)."},
        ],
        references=[
            ref("Maslen, E.N., Streltsov, V.A., Streltsova, N.R. (1993). X-ray study of the electron density in calcite, CaCO<sub>3</sub>. <i>Acta Crystallographica B</i> 49, 636–641.",
                "10.1107/S0108768193002575", "The cell used here.", ["lattice"]),
            ref("Gonzalez, L.A., Carpenter, S.J., Lohmann, K.C. (1992). Inorganic calcite morphology: roles of fluid chemistry and fluid flow. <i>Journal of Sedimentary Petrology</i> 62, 382–399.",
                "10.1306/D426790B-2B26-11D7-8648000102C1865D", "Speleothem calcite habit versus supersaturation.", ["morphology"]),
            ref("Davis, K.J., Dove, P.M., De Yoreo, J.J. (2000). The role of Mg<sup>2+</sup> as an impurity in calcite growth. <i>Science</i> 290, 1134–1137.",
                "10.1126/science.290.5494.1134", "AFM study of Mg effects on {101̄4} growth.", ["morphology"]),
            ref("Paquette, J., Reeder, R.J. (1995). Relationship between surface structure, growth mechanism, and trace element incorporation in calcite. <i>Geochimica et Cosmochimica Acta</i> 59, 735–749.",
                "10.1016/0016-7037(95)00004-J", "Step-specific trace-element uptake on {101̄4} growth hillocks.", ["geochemistry"]),
            ref("Roberts, N.M.W., Drost, K., Horstwood, M.S.A., Condon, D.J., Chew, D., Drake, H., et al. (2020). Laser ablation inductively coupled plasma mass spectrometry (LA-ICP-MS) U–Pb carbonate geochronology: strategies, progress, and limitations. <i>Geochronology</i> 2, 33–61.",
                "10.5194/gchron-2-33-2020", "Review of calcite U–Pb dating.", ["geochronology"]),
            ref("Ghosh, P., Adkins, J., Affek, H., Balta, B., Guo, W., Schauble, E.A., Schrag, D., Eiler, J.M. (2006). <sup>13</sup>C–<sup>18</sup>O bonds in carbonate minerals: a new kind of paleothermometer. <i>Geochimica et Cosmochimica Acta</i> 70, 1439–1456.",
                "10.1016/j.gca.2005.11.014", "Clumped-isotope thermometry.", ["thermometry"]),
        ] + SED_REFS,
    )


def dolomite_spec():
    forms = [
        form("10-14", (1, 0, -1, 4), "r, unit (cleavage) rhombohedron", "#e9d9c4"),
        form("0001", (0, 0, 0, 1), "c, basal pinacoid", "#b8a48c"),
        form("10-11", (1, 0, -1, 1), "M, steep rhombohedron", "#cdb08e"),
        form("01-18", (0, 1, -1, 8), "e, flat rhombohedron", "#d9c6ad"),
        form("11-20", (1, 1, -2, 0), "a, hexagonal prism", "#f2e7d8"),
    ]
    rows = _rows([
        ("C1", "tabular", "tabular, c{0001} at 0.35", [{"set": {"0001": 0.35}}]),
        ("C2", "thick", "thick tabular, c{0001} at 0.7", [{"set": {"0001": 0.7}}]),
        ("C0", "no c", "no basal pinacoid", []),
    ])
    cols = [
        {"code": "e", "label": "e", "detail": "flat e + a", "text": "flat rhombohedron e with prism a", "ops": [{"set": {"01-18": 1.0, "11-20": 1.0}}]},
        {"code": "r", "label": "r", "detail": "unit r", "text": "unit rhombohedron r", "ops": [{"set": {"10-14": 1.0}}]},
        {"code": "M", "label": "M", "detail": "steep M", "text": "steep rhombohedron M", "ops": [{"set": {"10-11": 1.0}}]},
        {"code": "ra", "label": "r+a", "detail": "r + prism a", "text": "r with hexagonal prism a", "ops": [{"set": {"10-14": 1.0, "11-20": 0.9}}]},
    ]
    return grid_spec(
        id="dolomite", name="Dolomite", formula="CaMg(CO₃)₂", group="Carbonates",
        chronometers="U–Pb carbonate dating; clumped isotopes; diagenetic thermometry",
        system="Trigonal", setting="R3̄, obverse hexagonal axes (point group 3̄; Dana (hkil) → (h k i 4l))",
        lattice=dict(a=4.812, b=4.812, c=16.02, gamma=120), lattice_source="Effenberger et al. (1981)", point_group="-3",
        forms=forms, base={}, rows=rows, cols=cols, elongation_axis=None, default=(2, 1), mono_color="#eadbc6",
        view={"tilt": 16, "turn": -20},
        title="Basal development × rhombohedron",
        subtitle="Dolomite's point group 3̄ has no mirror planes; it is the lower-symmetry cousin of calcite. Crystals are usually the unit rhombohedron r, sometimes the steep M, flattened on c or combined with the prism a.",
        row_title="Basal pinacoid", col_title="Rhombohedron / prism",
        note=("r∧r′ = 73.75° against Dana's 73°45′. Curved 'saddle' dolomite and non-planar (anhedral) textures are not "
              "convex polyhedra. Planar versus non-planar dolomite textures reflect a critical roughening temperature of "
              "about 50–100 °C (Gregg &amp; Sibley 1984)."),
        about="""
<p>Dolomite crystals are typically sharp unit rhombohedra, the "planar-e" texture of dolostones (Sibley &amp; Gregg 1987).
Above a roughening temperature of about 50–100 °C, faces become non-planar, and hot fluids grow curved saddle dolomite
(Radke &amp; Mathis 1980). Its point group 3̄ lacks the mirrors of calcite, and composition differs between growth sectors
(Reeder &amp; Prosky 1986).</p>""",
        habits=[
            {"name": "Rhombohedral (planar-e)", "text": "Unit rhombohedron r (row C0, column r)."},
            {"name": "Steep rhombohedral", "text": "M dominant (column M)."},
            {"name": "Tabular", "text": "Plates on c bevelled by r (row C1)."},
            {"name": "Saddle dolomite (not modelled)", "text": "Curved r faces."},
        ],
        references=[
            ref("Effenberger, H., Mereiter, K., Zemann, J. (1981). Crystal structure refinements of magnesite, calcite, rhodochrosite, siderite, smithonite, and dolomite, with discussion of some aspects of the stereochemistry of calcite type carbonates. <i>Zeitschrift für Kristallographie</i> 156, 233–243.",
                "10.1524/zkri.1981.156.14.233", "The cell used here.", ["lattice"]),
            ref("Gregg, J.M., Sibley, D.F. (1984). Epigenetic dolomitization and the origin of xenotopic dolomite texture. <i>Journal of Sedimentary Petrology</i> 54, 908–931.",
                "10.1306/212F8535-2B24-11D7-8648000102C1865D", "Planar versus non-planar dolomite and the critical roughening temperature.", ["morphology"]),
            ref("Sibley, D.F., Gregg, J.M. (1987). Classification of dolomite rock textures. <i>Journal of Sedimentary Petrology</i> 57, 967–975.",
                "10.1306/212F8CBA-2B24-11D7-8648000102C1865D", "The planar-e / planar-s / non-planar texture scheme.", ["morphology"]),
            ref("Radke, B.M., Mathis, R.L. (1980). On the formation and occurrence of saddle dolomite. <i>Journal of Sedimentary Petrology</i> 50, 1149–1168.",
                "10.1306/212F7B9E-2B24-11D7-8648000102C1865D", "Curved-face saddle dolomite and its formation conditions.", ["morphology"]),
            ref("Reeder, R.J., Prosky, J.L. (1986). Compositional sector zoning in dolomite. <i>Journal of Sedimentary Petrology</i> 56, 237–247.",
                "10.1306/212F88CD-2B24-11D7-8648000102C1865D", "Composition differs between growth sectors.", ["geochemistry"]),
        ],
    )


def aragonite_spec():
    forms = [
        form("110", (1, 1, 0), "m, rhombic prism", "#e3ead2"),
        form("010", (0, 1, 0), "b, side pinacoid", "#c7d3ad"),
        form("001", (0, 0, 1), "c, basal pinacoid", "#9fae80"),
        form("011", (0, 1, 1), "k, brachydome (chisel)", "#d9c98f"),
        form("021", (0, 2, 1), "i, steep brachydome", "#ead9a0"),
        form("111", (1, 1, 1), "p, rhombic dipyramid", "#b8c98e"),
    ]
    rows = _rows([
        ("T", "tabular", "thick tabular on (001)", [{"set": {"110": 1.0}}, {"set": {"001": 0.3}, "stage": 0.8}]),
        ("Q", "equant", "equant, d(m) = 1.0", [{"set": {"110": 1.0}}]),
        ("P", "prismatic", "prismatic, d(m) = 0.6", [{"set": {"110": 0.6}}]),
        ("A", "acicular", "acicular, d(m) = 0.3", [{"set": {"110": 0.3}}]),
    ])
    cols = [{"code": c, "label": c, "detail": det, "text": f"terminated by {det}", "ops": [{"set": {k: 1.0}}, {"rel": {"010": ["110", 1.0]}}]}
            for c, det, k in [("c", "c{001} flat", "001"), ("k", "k{011} chisel", "011"), ("i", "i{021} steep dome", "021"), ("p", "p{111} dipyramid", "111")]]
    return grid_spec(
        id="aragonite", name="Aragonite", formula="CaCO₃", group="Carbonates",
        chronometers="U-series dating (corals, speleothems); δ¹⁸O, Sr/Ca, clumped isotopes",
        system="Orthorhombic", setting="Pmcn (pseudo-hexagonal axis c; equals Dana's axes)",
        lattice=dict(a=4.96174, b=7.96918, c=5.74265), lattice_source="Antao &amp; Hassan (2009)", point_group="mmm",
        forms=forms, base={}, rows=rows, cols=cols, default=(2, 1), mono_color="#e2e8d0", view={"tilt": 14, "turn": -30},
        title="Prism length × termination",
        subtitle="The pseudo-hexagonal m{110} + b{010} prism (m∧m′ = 63.8°), from thick tablets to the needles of marine cements and ooids, with flat, chisel, steep-dome or dipyramidal ends.",
        row_title="Elongation along c", col_title="Termination",
        note=("m∧m′ = 63.81° against Dana's 63°48′. The pseudo-hexagonal cyclic trillings on {110} are twins and are not "
              "modelled. The Handbook of Mineralogy's 'prismatic along [010]' appears to be a setting slip; here the prism "
              "zone is [001], as in Dana."),
        about="""
<p>Aragonite is the high-pressure polymorph of CaCO₃ that nonetheless precipitates widely in seawater and in coral and
mollusc skeletons. Acicular aragonite needles form at high supersaturation and reactant supply (Given &amp; Wilkinson
1985), and seawater Mg/Ca and temperature decide whether aragonite or calcite precipitates (Morse et al. 1997).</p>""",
        habits=[
            {"name": "Acicular needles", "text": "Marine cements and ooid cortices (row A)."},
            {"name": "Chisel-terminated prism", "text": "m + b prism with k{011} (row P, column k)."},
            {"name": "Pseudo-hexagonal trilling (not modelled)", "text": "Cyclic twin on {110}."},
        ],
        references=[
            ref("Antao, S.M., Hassan, I. (2009). The orthorhombic structure of CaCO<sub>3</sub>, SrCO<sub>3</sub>, PbCO<sub>3</sub> and BaCO<sub>3</sub>: linear structural trends. <i>The Canadian Mineralogist</i> 47, 1245–1255.",
                "10.3749/canmin.47.5.1245", "The cell used here.", ["lattice"]),
            ref("Morse, J.W., Wang, Q., Tsio, M.Y. (1997). Influences of temperature and Mg:Ca ratio on CaCO<sub>3</sub> precipitates from seawater. <i>Geology</i> 25, 85–87.",
                "10.1130/0091-7613(1997)025<0085:IOTAMC>2.3.CO;2", "Temperature and Mg/Ca control on aragonite versus calcite.", ["morphology"]),
        ] + SED_REFS,
    )


# ----------------------------------------------------------------- sulfates
def gypsum_spec():
    forms = [
        form("010", (0, 1, 0), "b, side pinacoid (perfect cleavage)", "#f4f1ea"),
        form("120", (1, 2, 0), "m, prism", "#dcd6c8"),
        form("-111", (-1, 1, 1), "l, prism (termination)", "#c8bfa9"),
        form("-103", (-1, 0, 3), "e, pinacoid (lenticular faces)", "#b3a88e"),
    ]
    rows = _rows([
        ("A", "acicular", "acicular along c", [{"set": {"120": 0.3, "-111": 1.2}}]),
        ("P", "prismatic", "prismatic along c", [{"set": {"120": 0.55, "-111": 1.2}}]),
        ("S", "stubby", "stubby", [{"set": {"120": 1.0, "-111": 1.0}}]),
        ("F", "flattened ⊥ c", "flattened normal to c, no prism", [{"set": {"120": N, "-111": 0.7, "-103": 0.75}}]),
    ])
    cols = [
        {"code": "l", "label": "l", "detail": "l{1̄11}", "text": "l{1̄11} termination, b at 0.7", "ops": [{"set": {"010": 0.7}}]},
        {"code": "le", "label": "l+e", "detail": "l + e{1̄03}", "text": "l with e{1̄03}", "ops": [{"set": {"010": 0.7}}, {"rel": {"-103": ["-111", 1.0]}}]},
        {"code": "e", "label": "e", "detail": "e dominant", "text": "e{1̄03}-dominated lenticular termination", "ops": [{"set": {"010": 0.8}}, {"rel": {"-103": ["-111", 0.8]}}]},
        {"code": "s", "label": "sel", "detail": "thin (010) plate", "text": "thin selenite plate on (010)", "ops": [{"set": {"010": 0.3}}]},
    ]
    return grid_spec(
        id="gypsum", name="Gypsum", formula="CaSO₄·2H₂O", group="Sulfates",
        chronometers="Sr, S and O isotopes of evaporites; fluid inclusions",
        system="Monoclinic", setting="A2/a, b-unique (from I2/a; Dana (hkl) → ((h−l)/2, k, l))",
        lattice=dict(a=5.679, b=15.202, c=6.2865, beta=114.17), lattice_source="Pedersen &amp; Semmingsen (1982), transformed", point_group="2/m",
        forms=forms, base={"010": 0.7, "-111": 1.2}, rows=rows, cols=cols, default=(1, 0), mono_color="#efeae0",
        view={"tilt": 16, "turn": -40},
        title="Elongation × termination",
        subtitle="Gypsum runs from needles and prismatic selenite blades along c to lenticular crystals flattened normal to c. Experiments link prismatic crystals to clean brines and flattened l{1̄11} or lenticular e{1̄03} crystals to organic-rich, warmer brines (Cody &amp; Cody 1988).",
        row_title="Elongation", col_title="Termination / (010) tabularity",
        note=("Indices are in an A2/a cell whose c axis is Dana's morphological c. Seven of Dana's angles were reproduced, for "
              "example m∧m′ = 68.56° against 68°30′; offsets up to 0.3° come from a modern β that is 0.3° larger. Swallow-tail "
              "and Montmartre twins are not convex and are not modelled."),
        about="""
<p>Gypsum habit is a classic evaporite indicator. Without organics it grows prismatic. Dissolved organic matter and
higher temperature flatten it normal to c, first into {1̄11}-dominated crystals and then into lenticular crystals
bounded by curved e{1̄03} faces (Cody 1979; Cody &amp; Cody 1988). Twins such as the swallow-tail on (100) and the
Montmartre twin may be microbially induced (Cody &amp; Cody 1989).</p>""",
        habits=[
            {"name": "Selenite blades", "text": "Tabular on (010), elongated along c (column sel)."},
            {"name": "Prismatic", "text": "m prism capped by l (row P)."},
            {"name": "Lenticular", "text": "e-dominated lenses, flattened ⊥ c (row F, column e)."},
            {"name": "Twins (not modelled)", "text": "Swallow-tail and Montmartre twins."},
        ],
        references=[
            ref("Pedersen, B.F., Semmingsen, D. (1982). Neutron diffraction refinement of the structure of gypsum, CaSO<sub>4</sub>·2H<sub>2</sub>O. <i>Acta Crystallographica B</i> 38, 1074–1077.",
                "10.1107/S0567740882004993", "Structure; the cell is transformed to A2/a here.", ["lattice"]),
            ref("Heijnen, W.M.M., Hartman, P. (1991). Structural morphology of gypsum (CaSO<sub>4</sub>·2H<sub>2</sub>O), brushite (CaHPO<sub>4</sub>·2H<sub>2</sub>O) and pharmacolite (CaHAsO<sub>4</sub>·2H<sub>2</sub>O). <i>Journal of Crystal Growth</i> 108, 290–300.",
                "10.1016/0022-0248(91)90376-G", "Periodic-bond-chain (PBC) morphology of gypsum; note that its cell setting differs.", ["morphology"]),
            ref("Cody, R.D., Cody, A.M. (1988). Gypsum nucleation and crystal morphology in analog saline terrestrial environments. <i>Journal of Sedimentary Petrology</i> 58, 247–255.",
                "10.1306/212F8D69-2B24-11D7-8648000102C1865D", "Experiments: prismatic gypsum without organics; flattened, {111}-dominated or lenticular crystals with them.", ["morphology"]),
            ref("Cody, R.D. (1979). Lenticular gypsum: occurrences in nature, and experimental determinations of effects of soluble green plant material on its formation. <i>Journal of Sedimentary Petrology</i> 49, 1015–1028.",
                "10.1306/212F78A6-2B24-11D7-8648000102C1865D", "Lenticular habit and organic growth inhibitors.", ["morphology"]),
            ref("Cody, A.M., Cody, R.D. (1989). Evidence for micro-biological induction of {101} montmartre twinning of gypsum (CaSO<sub>4</sub>·2H<sub>2</sub>O). <i>Journal of Crystal Growth</i> 98, 721–730.",
                "10.1016/0022-0248(89)90310-2", "Montmartre twinning, which is not convex and is noted only.", ["morphology"]),
        ],
    )


def anhydrite_spec():
    forms = [
        form("010", (0, 1, 0), "c (Dana), pinacoid (perfect cleavage)", "#c9c4e0"),
        form("100", (1, 0, 0), "b (Dana), pinacoid", "#a9a2cf"),
        form("001", (0, 0, 1), "a (Dana), pinacoid", "#8a82bb"),
        form("101", (1, 0, 1), "m, rhombic prism", "#e1ddf0"),
        form("011", (0, 1, 1), "r, dome", "#d2cdea"),
    ]
    rows = _rows([(f"E{i + 1}", det, f"elongation along [100], d(a) = {v}", [{"set": {"100": v}}])
                  for i, (v, det) in enumerate([(1.0, "equant"), (1.6, "elongate"), (2.5, "prismatic ∥ a")])])
    cols = [{"code": f"b{i + 1}", "label": f"b{i + 1}", "detail": det, "text": f"(010) tabularity, d(b) = {v}", "ops": [{"set": {"010": v}}]}
            for i, (v, det) in enumerate([(1.0, "blocky"), (0.6, "tabular"), (0.35, "thin tabular")])]
    return grid_spec(
        id="anhydrite", name="Anhydrite", formula="CaSO₄", group="Sulfates",
        chronometers="Sr and S isotopes (seawater–hydrothermal mixing)",
        system="Orthorhombic", setting="Amma (Dana's morphological axes (a, b, c) = structural (c, a, b))",
        lattice=dict(a=7.006, b=6.998, c=6.245), lattice_source="Kirfel &amp; Will (1980)", point_group="mmm",
        forms=forms, base={"001": 1.0, "101": 1.3, "011": 1.25}, rows=rows, cols=cols, elongation_axis=(1, 0, 0),
        default=(0, 0), mono_color="#b7b0d8", view={"tilt": 18, "turn": -30},
        title="Elongation along a × tabularity on (010)",
        subtitle="Anhydrite crystals are near-rectangular blocks of three pinacoids parallel to its three cleavages, lightly bevelled by m{101} and r{011}. They can be elongated along a or tabular on (010).",
        row_title="Elongation along [100]", col_title="(010) tabularity",
        note=("Because a ≈ b, morphology alone barely separates {100} from {010}; the assignment follows the cleavage quality. "
              "Three Dana angles match to within 0.1°. Data linking habit to growth conditions are weak, so this matrix "
              "is descriptive."),
        about="""
<p>Anhydrite forms in evaporites and in seafloor hydrothermal systems, where its Sr isotopes record mixing of seawater
and vent fluid (Humphris &amp; Bach 2005). Crystals are blocky to tabular, dominated by the three cleavage pinacoids
predicted by periodic-bond-chain theory (Aquilano et al. 1992).</p>""",
        habits=[
            {"name": "Blocky", "text": "Three pinacoids of nearly equal size (cell E1b1)."},
            {"name": "Tabular on (010)", "text": "Column b3."},
            {"name": "Prismatic along a", "text": "Row E3."},
        ],
        references=[
            ref("Kirfel, A., Will, G. (1980). Charge density in anhydrite, CaSO<sub>4</sub>, from X-ray and neutron diffraction measurements. <i>Acta Crystallographica B</i> 36, 2881–2890.",
                "10.1107/S0567740880010461", "The cell used here.", ["lattice"]),
            ref("Aquilano, D., Rubbo, M., Catti, M., Pavese, A., Ugliengo, P. (1992). Theoretical equilibrium and growth morphology of anhydrite (CaSO<sub>4</sub>) crystals. <i>Journal of Crystal Growth</i> 125, 519–532.",
                "10.1016/0022-0248(92)90292-Q", "Hartman–Perdok morphology: {100}, {010} and {001} dominate.", ["morphology"]),
            ref("Humphris, S.E., Bach, W. (2005). On the Sr isotope and REE compositions of anhydrites from the TAG seafloor hydrothermal system. <i>Geochimica et Cosmochimica Acta</i> 69, 1511–1525.",
                "10.1016/j.gca.2004.10.004", "Anhydrite as a recorder of seawater–hydrothermal fluid mixing.", ["geochemistry"]),
        ],
    )


def barite_spec():
    forms = [
        form("001", (0, 0, 1), "c, basal pinacoid (perfect cleavage)", "#e9e3d6"),
        form("210", (2, 1, 0), "m, rhombic prism (Dana {110})", "#c9b99c"),
        form("101", (1, 0, 1), "d, dome (Dana {102})", "#d8c8a8"),
        form("011", (0, 1, 1), "o, dome", "#b49f7a"),
        form("211", (2, 1, 1), "z, dipyramid (Dana {111})", "#f0e6cf"),
    ]
    rows = _rows([(f"C{i + 1}", det, f"(001) tabularity, d(c) = {v}",
                   [{"set": {"001": v}}] + ([{"set": {"211": 1.05}}] if v == 1.0 else []))
                  for i, (v, det) in enumerate([(0.2, "thin tablet"), (0.4, "tabular"), (0.7, "thick tabular"), (1.0, "equant + z")])])
    cols = [
        {"code": "m", "label": "m", "detail": "rhombic {210}", "text": "rhombic tablet outlined by m{210}", "ops": [{"set": {"210": 1.0}}]},
        {"code": "mod", "label": "mod", "detail": "m + o + d", "text": "octagonal tablet, m + o + d", "ops": [{"set": {"210": 1.0, "011": 1.0, "101": 1.0}}]},
        {"code": "od", "label": "od", "detail": "o + d", "text": "rectangular tablet, o + d", "ops": [{"set": {"011": 1.0, "101": 1.0}}]},
        {"code": "o", "label": "o", "detail": "o dominant", "text": "elongated along [100], o dominant", "ops": [{"set": {"011": 0.8, "101": 1.3}}]},
    ]
    return grid_spec(
        id="barite", name="Barite", formula="BaSO₄", group="Sulfates",
        chronometers="Marine barite Sr and S isotopes; export-productivity proxy",
        system="Orthorhombic", setting="Pnma (a 8.88, b 5.45, c 7.16 Å; Dana (hkl) → (2h, k, l))",
        lattice=dict(a=8.88101, b=5.45447, c=7.15505), lattice_source="Antao (2012), permuted to Pnma", point_group="mmm",
        forms=forms, base={}, rows=rows, cols=cols, elongation_axis=None, default=(1, 1), mono_color="#e3dccb",
        view={"tilt": 30, "turn": -20},
        title="(001) tabularity × tablet outline",
        subtitle="Barite is typically tabular on its perfect cleavage c{001}. The outline is set by the side forms: rhombic with m{210}, octagonal with m + o + d, rectangular with o + d, or elongated along a when o dominates.",
        row_title="(001) tabularity", col_title="Tablet outline",
        note=("Dana's cell has a halved, so his m(110), d(102) and z(111) are {210}, {101} and {211} here. m∧m′ = 78.30° against "
              "78°22′. Rosettes, crested aggregates and micron-sized marine barite ellipsoids are not single convex crystals."),
        about="""
<p>Barite precipitates from seawater (marine barite), from seafloor hydrothermal and cold-seep fluids, and during
diagenesis. Crystal size and shape differ by origin, which helps distinguish them (Griffith &amp; Paytan 2012).
Experiments show that saturation, temperature, organics and Mg, Ca, Sr shift barite habit (Widanagamage et al. 2018).
Marine barite accumulation is a proxy for ocean export productivity (Paytan &amp; Griffith 2007).</p>""",
        habits=[
            {"name": "Rhombic tablet", "text": "c with m{210} (column m)."},
            {"name": "Octagonal / rectangular tablets", "text": "Bevelled by d and o (columns mod and od)."},
            {"name": "Prismatic along a", "text": "o dominant (column o)."},
        ],
        references=[
            ref("Antao, S.M. (2012). Structural trends for celestite (SrSO<sub>4</sub>), anglesite (PbSO<sub>4</sub>), and barite (BaSO<sub>4</sub>): confirmation of expected variations within the SO<sub>4</sub> groups. <i>American Mineralogist</i> 97, 661–665.",
                "10.2138/am.2012.3905", "The cell used here.", ["lattice"]),
            ref("Griffith, E.M., Paytan, A. (2012). Barite in the ocean – occurrence, geochemistry and palaeoceanographic applications. <i>Sedimentology</i> 59, 1817–1835.",
                "10.1111/j.1365-3091.2012.01327.x", "Barite origins, crystal size and shape, and proxy uses.", ["review", "morphology"]),
            ref("Paytan, A., Griffith, E.M. (2007). Marine barite: recorder of variations in ocean export productivity. <i>Deep-Sea Research II</i> 54, 687–705.",
                "10.1016/j.dsr2.2007.01.007", "Barite as an export-productivity proxy.", ["geochemistry"]),
            ref("Widanagamage, I.H., Waldron, A.R., Glamoclija, M. (2018). Controls on barite crystal morphology during abiotic precipitation. <i>Minerals</i> 8, 480.",
                "10.3390/min8110480", "Saturation, temperature, organics and cations as controls on barite habit.", ["morphology"]),
            ref("Shikazono, N. (1994). Precipitation mechanisms of barite in sulfate-sulfide deposits in back-arc basins. <i>Geochimica et Cosmochimica Acta</i> 58, 2203–2213.",
                "10.1016/0016-7037(94)90005-1", "Fluid mixing and supersaturation controls on precipitation.", ["morphology"]),
        ],
    )


# ----------------------------------------------------------------- cubic: halite, fluorite, pyrite, spinel
CUBE_OCT_ROWS = _rows([
    ("a", "cube", "cube", [{"set": {"100": 1.0, "111": N}}]),
    ("ao", "cube + minor o", "cube with small octahedron, d(o)/d(a) = 1.5", [{"set": {"100": 1.0, "111": 1.5}}]),
    ("co", "cubo-octahedron", "cubo-octahedron, d(o)/d(a) = 1.155", [{"set": {"100": 1.0, "111": 1.155}}]),
    ("oa", "octahedron + minor a", "octahedron with small cube, d(o)/d(a) = 0.75", [{"set": {"100": 1.0, "111": 0.75}}]),
    ("o", "octahedron", "octahedron", [{"set": {"100": N, "111": 0.577}}]),
])


def _cubic(id, name, formula, group, chronometers, a, pg, setting, forms, rows, cols, lattice_source, mono, title, subtitle,
           row_title, col_title, note, about, habits, refs, base=None, default=(0, 0)):
    return grid_spec(id=id, name=name, formula=formula, group=group, chronometers=chronometers, system="Cubic", setting=setting,
                     lattice=dict(a=a, b=a, c=a), lattice_source=lattice_source, point_group=pg, forms=forms, base=base or {},
                     rows=rows, cols=cols, elongation_axis=None, default=default, mono_color=mono, view={"tilt": 20, "turn": -28},
                     title=title, subtitle=subtitle, row_title=row_title, col_title=col_title, note=note, about=about,
                     habits=habits, references=refs)


def halite_spec():
    forms = [form("100", (1, 0, 0), "a, cube", "#e9eef2"), form("111", (1, 1, 1), "o, octahedron", "#bcd0de"),
             form("110", (1, 1, 0), "d, rhombic dodecahedron", "#d6e1ea")]
    cols = [{"code": c, "label": c, "detail": det, "text": det, "ops": [{"set": {"110": v}}]}
            for c, v, det in [("0", N, "no dodecahedron"), ("d1", 1.3, "minor d{110}"), ("d2", 1.2, "moderate d{110}")]]
    return _cubic("halite", "Halite", "NaCl", "Halides", "Fluid-inclusion paleothermometry; evaporite Br/Cl", 5.6404, "m-3m",
                  "Fm3̄m", forms, CUBE_OCT_ROWS, cols, "Handbook of Mineralogy", "#e4ebf0",
                  "Cube ↔ octahedron × dodecahedron",
                  "Halite grows as cubes; additives such as formamide, urea or Cd²⁺ stabilize {111} and turn cubes into octahedra.",
                  "Cube → octahedron", "Dodecahedron {110}",
                  "Cubic angles do not depend on the cell edge. Hopper and chevron halite are skeletal and not convex.",
                  """<p>Halite is the textbook cube, but its habit is very sensitive to additives. Formamide, urea and Cd²⁺
adsorb on {111} and stabilize octahedral faces (Radenovic et al. 2003, 2004, 2005), a habit change explained by
the role of water at the surface (van der Voort &amp; Hartman 1990). Skeletal hopper and chevron crystals record salt-pan
evaporation (Lowenstein &amp; Hardie 1985), and their fluid inclusions preserve brine temperatures (Roberts &amp; Spencer 1995).</p>""",
                  [{"name": "Cube", "text": "Row a."}, {"name": "Octahedron", "text": "Additive-induced (row o)."},
                   {"name": "Hopper / chevron (not modelled)", "text": "Skeletal, funnel-shaped cubes."}],
                  [ref("Radenovic, N., van Enckevort, W., Verwer, P., Vlieg, E. (2003). Growth and characteristics of the {111} NaCl crystal surface grown from solution. <i>Surface Science</i> 523, 307–315.",
                       "10.1016/S0039-6028(02)02463-9", "How octahedral {111} NaCl faces form from solution.", ["morphology"]),
                   ref("Radenovic, N., van Enckevort, W., Vlieg, E. (2004). Formamide adsorption and habit changes of alkali halide crystals grown from solutions. <i>Journal of Crystal Growth</i> 263, 544–551.",
                       "10.1016/j.jcrysgro.2003.11.103", "Additive-induced cube-to-octahedron habit change.", ["morphology"]),
                   ref("Radenovic, N., van Enckevort, W., Kaminski, D., Heijna, M., Vlieg, E. (2005). Structure of the {111} NaCl crystal surface grown from solution in the presence of CdCl<sub>2</sub>. <i>Surface Science</i> 599, 196–206.",
                       "10.1016/j.susc.2005.10.004", "Cd²⁺-stabilized octahedral faces.", ["morphology"]),
                   ref("van der Voort, E., Hartman, P. (1990). The role of water in the habit change from cube to octahedron of alkali halide crystals. <i>Journal of Crystal Growth</i> 104, 450–456.",
                       "10.1016/0022-0248(90)90146-C", "Theory of the cube/octahedron habit change.", ["morphology"]),
                   ref("Lowenstein, T.K., Hardie, L.A. (1985). Criteria for the recognition of salt-pan evaporites. <i>Sedimentology</i> 32, 627–644.",
                       "10.1111/j.1365-3091.1985.tb00478.x", "Hopper and chevron halite as depositional indicators.", ["morphology"]),
                   ref("Roberts, S.M., Spencer, R.J. (1995). Paleotemperatures preserved in fluid inclusions in halite. <i>Geochimica et Cosmochimica Acta</i> 59, 3929–3942.",
                       "10.1016/0016-7037(95)00253-V", "Fluid inclusions in chevron halite as a paleothermometer.", ["thermometry"])])


def fluorite_spec():
    forms = [form("100", (1, 0, 0), "a, cube", "#9b7fc9"), form("111", (1, 1, 1), "o, octahedron (cleavage)", "#c9b4e6"),
             form("110", (1, 1, 0), "d, rhombic dodecahedron", "#7aa6c9"), form("310", (3, 1, 0), "f, tetrahexahedron", "#b0d0e8"),
             form("421", (4, 2, 1), "t, hexoctahedron", "#e3d3f2")]
    cols = [{"code": c, "label": c, "detail": det, "text": det, "ops": [{"set": s}]}
            for c, s, det in [("0", {}, "no modifier"), ("d", {"110": 1.3}, "d{110} edges"), ("f", {"310": 1.03}, "f{310} edge bevels"),
                              ("t", {"421": 1.05}, "t{421} corner facets")]]
    return _cubic("fluorite", "Fluorite", "CaF₂", "Halides", "Sm–Nd dating of mineralization; REE fluid tracer", 5.462, "m-3m",
                  "Fm3̄m", forms, CUBE_OCT_ROWS, cols, "Cheetham et al. (1971)", "#a58bd0",
                  "Cube ↔ octahedron × modifier",
                  "Fluorite runs from cubes to octahedra, with edges bevelled by the tetrahexahedron f{310} and corners by the hexoctahedron t{421} (the Weardale style).",
                  "Cube → octahedron", "Modifier",
                  ("The often-repeated rule 'cubes at low temperature, octahedra at high' is not supported here by a verified "
                   "primary source, so the rows are descriptive. The Dana letter of the hexoctahedron is uncertain. Penetration "
                   "twins on {111} are not modelled."),
                  """<p>Fluorite's habit carries geochemistry: REE are taken up differently by {100} and {111} growth sectors
(Bosze &amp; Rakovan 2002). REE patterns trace hydrothermal fluids (Schwinn &amp; Markl 2005), and Sm–Nd dates fluorite
mineralization directly (Chesley et al. 1991).</p>""",
                  [{"name": "Cube", "text": "Row a."}, {"name": "Octahedron", "text": "Row o."},
                   {"name": "Bevelled cube", "text": "f{310} or t{421} modifiers (columns f and t)."}],
                  [ref("Cheetham, A.K., Fender, B.E.F., Cooper, M.J. (1971). Defect structure of calcium fluoride containing excess anions I. Bragg scattering. <i>Journal of Physics C</i> 4, 3107–3121.",
                       "10.1088/0022-3719/4/18/016", "Structure and cell.", ["lattice"]),
                   ref("Bosze, S., Rakovan, J. (2002). Surface-structure-controlled sectoral zoning of the rare earth elements in fluorite from Long Lake, New York, and Bingham, New Mexico, USA. <i>Geochimica et Cosmochimica Acta</i> 66, 997–1009.",
                       "10.1016/S0016-7037(01)00822-5", "REE uptake differs between {100} and {111} sectors.", ["geochemistry", "morphology"]),
                   ref("Schwinn, G., Markl, G. (2005). REE systematics in hydrothermal fluorite. <i>Chemical Geology</i> 216, 225–248.",
                       "10.1016/j.chemgeo.2004.11.012", "Fluorite REE as fluid tracers.", ["geochemistry"]),
                   ref("Chesley, J.T., Halliday, A.N., Scrivener, R.C. (1991). Samarium-neodymium direct dating of fluorite mineralization. <i>Science</i> 252, 949–951.",
                       "10.1126/science.252.5008.949", "Sm–Nd fluorite geochronology.", ["geochronology"])])


def pyrite_spec():
    forms = [form("100", (1, 0, 0), "a, cube (striated)", "#d6b84a"), form("111", (1, 1, 1), "o, octahedron", "#b8973a"),
             form("210", (2, 1, 0), "e, pyritohedron", "#e9d27a")]
    cols = [{"code": c, "label": c, "detail": det, "text": det, "ops": [{"set": {"210": v}}]}
            for c, v, det in [("0", N, "no pyritohedron"), ("e1", 1.25, "minor e{210}"), ("e2", 1.05, "moderate e{210}"), ("e3", 0.89, "pyritohedron dominant")]]
    return _cubic("pyrite", "Pyrite", "FeS₂", "Sulfides", "Re–Os dating; trace-element (Au, As) zoning; S isotopes", 5.4179, "m-3",
                  "Pa3̄ (point group m3̄)", forms, CUBE_OCT_ROWS, cols, "Handbook of Mineralogy", "#d4b553",
                  "Cube ↔ octahedron × pyritohedron",
                  "Pyrite's point group m3̄ lacks the diagonal mirrors of a true cube, so {210} is the 12-faced pentagonal pyritohedron. In experiments, morphology moves from cube to octahedron to pyritohedron as temperature and supersaturation rise (Murowchick &amp; Barnes 1987).",
                  "Cube → octahedron", "Pyritohedron {210}",
                  ("Which of {210} or {120} is the 'positive' pyritohedron is fixed only relative to other pyrite forms; its "
                   "absolute link to the Pa3̄ structure is not established here. Iron-cross twins and framboids are not single convex crystals."),
                  """<p>Pyrite is the most common sulfide, and its habit tracks growth conditions: in hydrothermal experiments
needles form at low temperature and low supersaturation, with cubes, octahedra and then pyritohedra as temperature and
supersaturation increase (Murowchick &amp; Barnes 1987). Its trace-element zoning (Large et al. 2009) and Re–Os
(Stein et al. 2000) make it a petrochronometer of ore fluids. The size of framboids, aggregates of tiny crystals, is a
redox proxy (Wilkin et al. 1996).</p>""",
                  [{"name": "Striated cube", "text": "Row a, column 0."}, {"name": "Pyritohedron", "text": "Column e3."},
                   {"name": "Pseudo-icosahedron", "text": "Octahedron + pyritohedron (row o, columns e2–e3)."}],
                  [ref("Murowchick, J.B., Barnes, H.L. (1987). Effects of temperature and degree of supersaturation on pyrite morphology. <i>American Mineralogist</i> 72, 1241–1250.",
                       None, "Hydrothermal experiments relating cube, octahedron and pyritohedron to temperature and supersaturation.", ["morphology"], url="http://www.minsocam.org/ammin/AM72/AM72_1241.pdf"),
                   ref("Brostigen, G., Kjekshus, A. (1969). Redetermined crystal structure of FeS<sub>2</sub> (pyrite). <i>Acta Chemica Scandinavica</i> 23, 2186–2188.",
                       "10.3891/acta.chem.scand.23-2186", "Structure.", ["lattice"]),
                   ref("Barnard, A.S., Russo, S.P. (2007). Shape and thermodynamic stability of pyrite FeS<sub>2</sub> nanocrystals and nanorods. <i>The Journal of Physical Chemistry C</i> 111, 11742–11746.",
                       "10.1021/jp0738199", "First-principles shape model including the pyritohedron.", ["morphology"]),
                   ref("Wilkin, R.T., Barnes, H.L., Brantley, S.L. (1996). The size distribution of framboidal pyrite in modern sediments: an indicator of redox conditions. <i>Geochimica et Cosmochimica Acta</i> 60, 3897–3912.",
                       "10.1016/0016-7037(96)00209-8", "Framboid size as a redox proxy.", ["geochemistry"]),
                   ref("Large, R.R., Danyushevsky, L.V., Hollit, C., Maslennikov, V., Meffre, S., Gilbert, S., et al. (2009). Gold and trace element zonation in pyrite using a laser imaging technique: implications for the timing of gold in orogenic and Carlin-style sediment-hosted deposits. <i>Economic Geology</i> 104, 635–668.",
                       "10.2113/gsecongeo.104.5.635", "LA-ICP-MS trace-element zoning in pyrite.", ["geochemistry"]),
                   ref("Stein, H.J., Morgan, J.W., Scherstén, A. (2000). Re-Os dating of low-level highly radiogenic (LLHR) sulfides: the Harnäs gold deposit, southwest Sweden, records continental-scale tectonic events. <i>Economic Geology</i> 95, 1657–1671.",
                       "10.2113/gsecongeo.95.8.1657", "Re–Os sulfide geochronology.", ["geochronology"])])


def spinel_spec():
    forms = [form("111", (1, 1, 1), "o, octahedron", "#a33a4a"), form("110", (1, 1, 0), "d, rhombic dodecahedron", "#cf6a77"),
             form("100", (1, 0, 0), "a, cube", "#e9a3ac")]
    rows = _rows([(c, det, f"dodecahedron {det}", [{"set": {"110": v}}]) for c, v, det in
                  [("d0", N, "absent"), ("d1", 1.15, "minor"), ("d2", 1.08, "moderate"), ("d3", 1.0, "strong")]])
    cols = [{"code": c, "label": c, "detail": det, "text": f"cube {det}", "ops": [{"set": {"100": v}}]}
            for c, v, det in [("a0", N, "absent"), ("a1", 1.5, "minor"), ("a2", 1.3, "moderate")]]
    return _cubic("spinel", "Spinel / chromite", "MgAl₂O₄ – FeCr₂O₄", "Oxides", "Cr# as a melting and tectonic-setting indicator", 8.0898,
                  "m-3m", "Fd3̄m", forms, rows, cols, "Handbook of Mineralogy; Finger et al. (1986)", "#a8404f",
                  "Octahedron with dodecahedron and cube",
                  "Spinel-group minerals, including chromite and magnesiochromite, which share the structure, grow as octahedra whose edges and corners may be truncated by d{110} and a{100}.",
                  "Dodecahedron {110}", "Cube {100}",
                  ("Chromite (a ≈ 8.34 Å) has the same Fd3̄m structure and the same convex habits. Spinel-law twins on {111} and "
                   "the skeletal, hopper and dendritic crystals of rapidly grown chromian spinel are not modelled."),
                  """<p>Chromian spinel is a key petrogenetic indicator: its Cr# records the degree of mantle melting and the tectonic
setting (Dick &amp; Bullen 1984; Barnes &amp; Roeder 2001). In MORB, rapid diffusion-controlled growth produces
skeletal and hopper crystals whose Cr# zoning follows their morphology (Roeder et al. 2001). Magnetite, on its own page,
is the Fe³⁺ member of the same spinel structure.</p>""",
                  [{"name": "Octahedron", "text": "Row d0, column a0."}, {"name": "Edge-bevelled", "text": "d{110} truncations (rows d1–d3)."}],
                  [ref("Finger, L.W., Hazen, R.M., Hofmeister, A.M. (1986). High-pressure crystal chemistry of spinel (MgAl<sub>2</sub>O<sub>4</sub>) and magnetite (Fe<sub>3</sub>O<sub>4</sub>): comparisons with silicate spinels. <i>Physics and Chemistry of Minerals</i> 13, 215–220.",
                       "10.1007/BF00308271", "Structure.", ["lattice"]),
                   ref("Bosi, F., Biagioni, C., Pasero, M. (2019). Nomenclature and classification of the spinel supergroup. <i>European Journal of Mineralogy</i> 31, 183–192.",
                       "10.1127/ejm/2019/0031-2788", "Current spinel-supergroup nomenclature.", ["review"]),
                   ref("Dick, H.J.B., Bullen, T. (1984). Chromian spinel as a petrogenetic indicator in abyssal and alpine-type peridotites and spatially associated lavas. <i>Contributions to Mineralogy and Petrology</i> 86, 54–76.",
                       "10.1007/BF00373711", "Cr# as an indicator of melting and tectonic setting.", ["petrology"]),
                   ref("Barnes, S.J., Roeder, P.L. (2001). The range of spinel compositions in terrestrial mafic and ultramafic rocks. <i>Journal of Petrology</i> 42, 2279–2302.",
                       "10.1093/petrology/42.12.2279", "Compositional fields of chromian spinel by rock type.", ["petrology"]),
                   ref("Roeder, P.L., Poustovetov, A., Oskarsson, N. (2001). Growth forms and composition of chromian spinel in MORB magma: diffusion-controlled crystallization of chromian spinel. <i>The Canadian Mineralogist</i> 39, 397–416.",
                       "10.2113/gscanmin.39.2.397", "Skeletal and hopper chromian spinel; morphology tied to Cr# zoning.", ["morphology"])],
                  base={"111": 1.0})


def ilmenite_spec():
    forms = [
        form("0001", (0, 0, 0, 1), "c, basal pinacoid", "#2f2f35"),
        form("01-12", (0, 1, -1, 2), "r, unit rhombohedron", "#5a5a66"),
        form("11-20", (1, 1, -2, 0), "a, hexagonal prism", "#7c7c8a"),
        form("2-1-13", (2, -1, -1, 3), "n, second-kind rhombohedron", "#9a9aa8"),
        form("10-14", (1, 0, -1, 4), "e, rhombohedron", "#b8b8c4"),
    ]
    rows = _rows([(f"C{i + 1}", det, f"basal c{{0001}} at {v}", [{"set": {"0001": v}}])
                  for i, (v, det) in enumerate([(0.15, "thin plate"), (0.3, "platy"), (0.5, "thick tabular"), (0.95, "rhombohedral")])])
    cols = [{"code": c, "label": c, "detail": det, "text": f"lateral forms {det}", "ops": [{"set": s}]}
            for c, s, det in [("r", {}, "r only"), ("ra", {"11-20": 1.0}, "r + a{112̄0}"), ("rn", {"2-1-13": 0.95}, "r + n{21̄1̄3}"),
                              ("re", {"10-14": 0.75}, "r + e{101̄4}")]]
    return grid_spec(
        id="ilmenite", name="Ilmenite", formula="FeTiO₃", group="Oxides",
        chronometers="Fe–Ti two-oxide thermometry and oxybarometry; remanence (hemo-ilmenite)",
        system="Trigonal", setting="R3̄, obverse hexagonal axes (point group 3̄; Dana (hkil) → (h k i −2l))",
        lattice=dict(a=5.08854, b=5.08854, c=14.0924, gamma=120), lattice_source="Handbook of Mineralogy; Wechsler &amp; Prewitt (1984)",
        point_group="-3", forms=forms, base={"01-12": 1.0}, rows=rows, cols=cols, elongation_axis=None, default=(1, 0),
        mono_color="#3c3c44", view={"tilt": 30, "turn": -20},
        title="Tabularity × lateral forms",
        subtitle="Ilmenite is thick tabular to platy on c{0001}, bounded by the rhombohedron r{011̄2}. With point group 3̄ (no mirrors) the n{21̄1̄3} faces form a 'rhombohedron of the second kind' rather than a hexagonal dipyramid.",
        row_title="Tabularity", col_title="Lateral forms",
        note=("Dana's morphological c is half the structural c. His positive rhombohedron maps to {011̄2} in the obverse cell "
              "(l doubles and changes sign), reproducing r∧r′ = 94.49° against 94°29′. The absolute sense of the second-kind "
              "forms cannot be fixed by goniometry alone. Exsolution lamellae and skeletal quench crystals are not modelled."),
        about="""
<p>Ilmenite and magnetite together are the Fe–Ti two-oxide thermometer and oxybarometer (Buddington &amp; Lindsley 1964;
Ghiorso &amp; Evans 2008). Ilmenite crystals are tabular on c, and in many rocks ilmenite occurs as exsolution lamellae
in magnetite or hematite (Haggerty 1991). Hemo-ilmenite intergrowths carry strong, stable remanence.</p>""",
        habits=[
            {"name": "Thick tabular", "text": "c + r (row C3)."},
            {"name": "Thin plate", "text": "Row C1."},
            {"name": "With n bevels", "text": "Second-kind rhombohedron (column rn)."},
        ],
        references=[
            ref("Wechsler, B.A., Prewitt, C.T. (1984). Crystal structure of ilmenite (FeTiO<sub>3</sub>) at high temperature and at high pressure. <i>American Mineralogist</i> 69, 176–185.",
                None, "Structure refinement.", ["lattice"], url="http://www.minsocam.org/ammin/AM69/AM69_176.pdf"),
            ref("Buddington, A.F., Lindsley, D.H. (1964). Iron-titanium oxide minerals and synthetic equivalents. <i>Journal of Petrology</i> 5, 310–357.",
                "10.1093/petrology/5.2.310", "Magnetite–ilmenite thermometry, oxybarometry and exsolution.", ["thermometry"]),
            ref("Ghiorso, M.S., Evans, B.W. (2008). Thermodynamics of rhombohedral oxide solid solutions and a revision of the Fe-Ti two-oxide geothermometer and oxygen-barometer. <i>American Journal of Science</i> 308, 957–1039.",
                "10.2475/09.2008.01", "The current Fe–Ti two-oxide thermometer.", ["thermometry"]),
            ref("Haggerty, S.E. (1991). Oxide textures – a mini-atlas. <i>Reviews in Mineralogy</i> 25, 129–220.",
                "10.1515/9781501508684-008", "Textures and growth forms of Fe–Ti oxides, including lamellae and skeletal crystals.", ["morphology"]),
        ],
    )
