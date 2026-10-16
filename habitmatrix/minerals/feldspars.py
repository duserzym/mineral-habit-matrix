"""K-feldspar (C2/m) and plagioclase (low albite, C-1).  Dana's feldspar axes equal the
structural ones: his 'β = 63°57′' is the interfacial angle (001)∧(100), so no sign flip."""

from ._common import ref
from ._grid import form, grid_spec

N = None

SHARED_REFS = [
    ref("Smith, J.V., Brown, W.L. (1988). <i>Feldspar Minerals</i>, Vol. 1, 2nd ed. Springer.",
        "10.1007/978-3-642-72594-4", "The standard reference for feldspar crystallography and morphology.", ["review"]),
    ref("Higgins, M.D. (1994). Numerical modeling of crystal shapes in thin sections: estimation of crystal habit and true size. <i>American Mineralogist</i> 79, 113–119.",
        None, "Recovering 3D habit from 2D sections.", ["geometry"], url="http://www.minsocam.org/ammin/AM79/AM79_113.pdf"),
    ref("Morgan, D.J., Jerram, D.A. (2006). On estimating crystal shape for crystal size distribution analysis. <i>Journal of Volcanology and Geothermal Research</i> 154, 1–7.",
        "10.1016/j.jvolgeores.2005.09.016", "Estimating short:intermediate:long shape for crystal size distributions.", ["geometry"]),
]


def kfs_spec():
    forms = [
        form("010", (0, 1, 0), "b, side pinacoid (M)", "#e7c9a9"),
        form("001", (0, 0, 1), "c, basal pinacoid (P)", "#d29a70"),
        form("110", (1, 1, 0), "m, prism (T, l)", "#f1dcc4"),
        form("-101", (-1, 0, 1), "x, pinacoid", "#b77c58"),
        form("-201", (-2, 0, 1), "y, pinacoid", "#c99a7a"),
        form("021", (0, 2, 1), "n, prism (Baveno plane)", "#a7684a"),
    ]
    rows = [
        {"code": "A", "label": "B0", "detail": "b minor (adularia-like)", "text": "b{010} minor, d(b)/d(m) = 1.5", "ops": [{"rel": {"010": ["110", 1.5]}}]},
        {"code": "1", "label": "B1", "detail": "blocky", "text": "blocky, d(b)/d(m) = 1.0", "ops": [{"rel": {"010": ["110", 1.0]}}]},
        {"code": "2", "label": "B2", "detail": "d(b)/d(m) 0.6", "text": "flattened on (010), d(b)/d(m) = 0.6", "ops": [{"rel": {"010": ["110", 0.6]}}]},
        {"code": "3", "label": "B3", "detail": "0.35", "text": "tabular on (010), d(b)/d(m) = 0.35", "ops": [{"rel": {"010": ["110", 0.35]}}]},
        {"code": "4", "label": "B4", "detail": "thin tablet", "text": "thin sanidine tablet, d(b)/d(m) = 0.2", "ops": [{"rel": {"010": ["110", 0.2]}}]},
    ]
    cols = [
        {"code": "a", "label": "[100]+", "detail": "elongate ∥ a", "text": "elongated along [100], square c–b section", "ops": [{"set": {"001": 1.0, "110": 2.6, "-101": 2.4, "-201": 3.0, "021": 1.15}}]},
        {"code": "b", "label": "[100]", "detail": "mild ∥ a", "text": "mildly elongated along [100]", "ops": [{"set": {"001": 1.0, "110": 1.6, "-101": 1.5, "-201": 1.75, "021": 1.2}}]},
        {"code": "e", "label": "eq", "detail": "equant", "text": "equant", "ops": [{"set": {"001": 1.0, "110": 1.0, "-101": 1.1, "-201": 1.3}}]},
        {"code": "c", "label": "[001]", "detail": "mild ∥ c", "text": "mildly prismatic along [001]", "ops": [{"set": {"001": 1.5, "110": 1.0, "-101": 1.5, "-201": 1.75}}]},
        {"code": "p", "label": "[001]+", "detail": "prismatic ∥ c", "text": "prismatic along [001] (Carlsbad habit)", "ops": [{"set": {"001": 2.7, "110": 1.0, "-101": 2.7, "-201": 3.1}}]},
    ]
    return grid_spec(
        id="k-feldspar", name="K-feldspar", formula="KAlSi₃O₈", group="Framework silicates",
        chronometers="⁴⁰Ar/³⁹Ar multi-diffusion-domain (MDD) thermochronology; Pb isotopes",
        system="Monoclinic", setting="C2/m (orthoclase/sanidine), obtuse β",
        lattice=dict(a=8.5632, b=12.963, c=7.2099, beta=116.073), lattice_source="Prince et al. (1973), orthoclase", point_group="2/m",
        forms=forms, base={}, rows=rows, cols=cols, default=(2, 2), mono_color="#e3c3a3", view={"tilt": 16, "turn": -40},
        elongation_axis=(0, 0, 1),
        title="Flattening on (010) × elongation axis",
        subtitle="Rows flatten the crystal on b{010}, from adularia-like crystals to thin sanidine tablets. Columns move the elongation from [100] (square c–b section, the shape of Baveno-twinned crystals) through equant to [001] (the Carlsbad-type prism).",
        row_title="(010) flattening", col_title="Elongation",
        note=("Eight interfacial angles match Dana (1892) to within 0.2°, for example c∧x = 50.21° against 50°16.5′. Sanidine, "
              "orthoclase and adularia cells differ by less than 0.5%. Microcline (C1̄) has the same forms and habits. Carlsbad, "
              "Baveno and Manebach are twin laws, not single convex crystals, so they are not modelled. The Handbook of "
              "Mineralogy's orthoclase c = 7.299 Å is a typo for 7.2099 Å."),
        about="""
<p>K-feldspar is built from a handful of forms: the pinacoids b{010} and c{001}, the prism m{110} and the pinacoids
x{1̄01} and y{2̄01}. Changing their relative sizes moves the crystal between tablets flattened on (010) (sanidine),
prisms along c, crystals elongated along a, and the pseudo-orthorhombic adularia of Alpine veins. Megacrysts in granites
are phenocrysts with inclusion zoning (Vernon 1986), and their size distributions record thermal history (Higgins 1999).
In thermochronology, K-feldspar's internal diffusion domains are modelled with the MDD approach (Lovera et al. 1989).</p>""",
        habits=[
            {"name": "Prismatic ∥ c", "text": "b + m prism with c, x, y ends: common orthoclase and the habit of Carlsbad twins (column [001]+)."},
            {"name": "Elongated ∥ a", "text": "A square c–b prism, as in Baveno-twinned crystals (column [100]+)."},
            {"name": "Adularia", "text": "m + x + c with little b: pseudo-orthorhombic or rhombohedral-looking (row B0)."},
            {"name": "Sanidine tablets", "text": "Tabular on (010), typical of volcanic sanidine (rows B3–B4)."},
        ],
        references=[
            ref("Prince, E., Donnay, G., Martin, R.F. (1973). Neutron diffraction refinement of an ordered orthoclase structure. <i>American Mineralogist</i> 58, 500–507.",
                None, "The cell used here.", ["lattice"], url="http://www.minsocam.org/ammin/AM58/AM58_500.pdf"),
            ref("Vernon, R.H. (1986). K-feldspar megacrysts in granites — phenocrysts, not porphyroblasts. <i>Earth-Science Reviews</i> 23, 1–63.",
                "10.1016/0012-8252(86)90003-6", "Origin, habit and inclusion zoning of megacrysts.", ["morphology"]),
            ref("Higgins, M.D. (1999). Origin of megacrysts in granitoids by textural coarsening: a crystal size distribution (CSD) study of microcline in the Cathedral Peak Granodiorite. <i>Geological Society, London, Special Publications</i> 168, 207–219.",
                "10.1144/GSL.SP.1999.168.01.14", "K-feldspar crystal size distributions and thermal history.", ["geometry"]),
            ref("Lovera, O.M., Richter, F.M., Harrison, T.M. (1989). The <sup>40</sup>Ar/<sup>39</sup>Ar thermochronometry for slowly cooled samples having a distribution of diffusion domain sizes. <i>Journal of Geophysical Research</i> 94, 17917–17935.",
                "10.1029/JB094iB12p17917", "K-feldspar MDD thermochronology.", ["thermochronology"]),
        ] + SHARED_REFS,
    )


def plag_spec():
    forms = [
        form("010", (0, 1, 0), "b, pinacoid (M; albite twin plane)", "#e9eef3"),
        form("001", (0, 0, 1), "c, pinacoid (P)", "#b9c6d3"),
        form("110", (1, 1, 0), "m, pinacoid", "#d4dde7"),
        form("1-10", (1, -1, 0), "M, pinacoid", "#a3b2c2"),
        form("-101", (-1, 0, 1), "x, pinacoid", "#8a9bb0"),
        form("-201", (-2, 0, 1), "y, pinacoid", "#c7d1dc"),
    ]
    rows = [
        {"code": "1", "label": "S1", "detail": "blocky", "text": "blocky, d(b)/d(c) = 1.0", "ops": [{"set": {"010": 1.0}}]},
        {"code": "2", "label": "S2", "detail": "0.6", "text": "tabular on (010), d(b)/d(c) = 0.6", "ops": [{"set": {"010": 0.6}}]},
        {"code": "3", "label": "S3", "detail": "0.4", "text": "tabular, d(b)/d(c) = 0.4", "ops": [{"set": {"010": 0.4}}]},
        {"code": "4", "label": "S4", "detail": "0.25", "text": "lath-like, d(b)/d(c) = 0.25", "ops": [{"set": {"010": 0.25}}]},
        {"code": "5", "label": "S5", "detail": "platy", "text": "platy (cleavelandite), d(b)/d(c) = 0.12", "ops": [{"set": {"010": 0.12}}]},
    ]

    def elong(f):
        return {"set": {"110": f, "1-10": f, "-101": 1.1 * f, "-201": 1.35 * f}}

    cols = [
        {"code": "a", "label": "I1", "detail": "equant in (010)", "text": "equant in the (010) plane", "ops": [elong(1.0)]},
        {"code": "b", "label": "I1.5", "detail": "1.5", "text": "elongated along [100], d(m)/d(c) = 1.5", "ops": [elong(1.5)]},
        {"code": "c", "label": "I2.5", "detail": "2.5", "text": "elongated along [100], d(m)/d(c) = 2.5", "ops": [elong(2.5)]},
        {"code": "d", "label": "I4", "detail": "lath", "text": "lath elongated along [100], d(m)/d(c) = 4", "ops": [elong(4.0)]},
    ]
    return grid_spec(
        id="plagioclase", name="Plagioclase", formula="NaAlSi₃O₈ – CaAl₂Si₂O₈", group="Framework silicates",
        chronometers="Diffusion chronometry (Mg, Sr); crystal size distributions; ⁴⁰Ar/³⁹Ar",
        system="Triclinic", setting="C1̄ (low albite; anorthite P1̄ uses (h k 2l))",
        lattice=dict(a=8.142, b=12.785, c=7.159, alpha=94.19, beta=116.61, gamma=87.68),
        lattice_source="Harlow &amp; Brown (1980), low albite", point_group="-1",
        forms=forms, base={"001": 1.0}, rows=rows, cols=cols, default=(2, 1), mono_color="#d7dee6",
        view={"tilt": 16, "turn": -40}, elongation_axis=(1, 0, 0),
        title="(010) tabularity × elongation along [100]",
        subtitle="Point group 1̄ makes every face its own pinacoid: m and M, and x and y, are independent forms. Rows flatten the crystal on b{010}; columns stretch it along [100] into the igneous lath.",
        row_title="(010) tabularity (S/I)", col_title="Elongation along [100] (I/L)",
        note=("Seven interfacial angles match Dana (1892) albite to within 0.25°, for example (010)∧(001) = 86.47° against "
              "86°24′. The [100] lath axis follows common petrographic usage but was not confirmed from a primary source; "
              "[001]-elongated (anorthite-type) and [010]-elongated (pericline) habits also occur. Albite and pericline "
              "polysynthetic twinning cannot be shown as a single convex crystal."),
        about="""
<p>Plagioclase is triclinic, so its only symmetry is inversion and each pair of parallel faces is a separate pinacoid.
That is why m{110} and M{11̄0} can be developed differently. Igneous plagioclase is tabular on (010), and its 3D
proportions (short : intermediate : long) record crystallization conditions: experiments relate morphology to undercooling
(Lofgren 1974), 3D reconstructions show variable S/I at near-constant I/L (Duchene et al. 2008), and aspect ratio in
dolerites tracks crystallization time (Holness 2014). Those 3D proportions are exactly the axes of this matrix.</p>""",
        habits=[
            {"name": "Tabular on (010)", "text": "The default habit, d(b) about half of d(c) (row S2)."},
            {"name": "Igneous lath", "text": "Flattened on (010) and elongated along [100] (rows S3–S4, columns I2.5–I4)."},
            {"name": "Cleavelandite", "text": "Platy pegmatitic albite (row S5)."},
            {"name": "Not modelled", "text": "Pericline albite elongated along b, anorthite-type prisms along c, and all polysynthetic twins."},
        ],
        references=[
            ref("Harlow, G.E., Brown, G.E. Jr. (1980). Low albite: an X-ray and neutron diffraction study. <i>American Mineralogist</i> 65, 986–995.",
                None, "The cell used here.", ["lattice"], url="http://www.minsocam.org/ammin/AM65/AM65_986.pdf"),
            ref("Lofgren, G. (1974). An experimental study of plagioclase crystal morphology; isothermal crystallization. <i>American Journal of Science</i> 274, 243–273.",
                "10.2475/ajs.274.3.243", "Plagioclase morphology (tabular → skeletal → spherulitic) versus undercooling.", ["morphology"]),
            ref("Duchene, S., Pupier, E., De Veslud, C.L.C., Toplis, M.J. (2008). A 3D reconstruction of plagioclase crystals in a synthetic basalt. <i>American Mineralogist</i> 93, 893–901.",
                "10.2138/am.2008.2679", "3D short:intermediate:long proportions of experimental plagioclase.", ["geometry"]),
            ref("Holness, M.B. (2014). The effect of crystallization time on plagioclase grain shape in dolerites. <i>Contributions to Mineralogy and Petrology</i> 168, 1076.",
                "10.1007/s00410-014-1076-5", "Plagioclase aspect ratio as a record of crystallization time.", ["morphology", "chronometry"]),
            ref("Costa, F., Dohmen, R., Chakraborty, S. (2008). Time scales of magmatic processes from modeling the zoning patterns of crystals. <i>Reviews in Mineralogy and Geochemistry</i> 69, 545–594.",
                "10.2138/rmg.2008.69.14", "Diffusion chronometry, including plagioclase.", ["chronometry"]),
            ref("Angel, R.J., Carpenter, M.A., Finger, L.W. (1990). Structural variation associated with compositional variation and order-disorder behavior in anorthite-rich feldspars. <i>American Mineralogist</i> 75, 150–162.",
                None, "The anorthite cell, for the An end-member.", ["lattice"], url="http://www.minsocam.org/ammin/AM75/AM75_150.pdf"),
        ] + SHARED_REFS,
    )
