"""Olivine (forsterite–Fo90), Pbnm setting = Dana/Koksharov morphological axes."""

from ._common import ref
from ._grid import form, grid_spec

ID = "olivine"
N = None

FORMS = [
    form("010", (0, 1, 0), "b, side pinacoid", "#6f8f3a"),
    form("110", (1, 1, 0), "m, prism", "#9fb84a"),
    form("120", (1, 2, 0), "s, prism", "#c2cf6a"),
    form("100", (1, 0, 0), "a, front pinacoid", "#4f6b2c"),
    form("021", (0, 2, 1), "k, dome", "#d9c85a"),
    form("101", (1, 0, 1), "d, dome", "#b49a3c"),
    form("111", (1, 1, 1), "e, dipyramid", "#e6dc9a"),
    form("001", (0, 0, 1), "c, basal pinacoid", "#8a7a3a"),
]

ROWS = [
    {"code": "T2", "label": "T2", "detail": "tabular (010)", "text": "strongly tabular on (010)", "ops": [{"set": {"010": 0.42}}]},
    {"code": "T1", "label": "T1", "detail": "mildly tabular", "text": "mildly tabular on (010)", "ops": [{"set": {"010": 0.66}}]},
    {"code": "Q", "label": "Q", "detail": "equant", "text": "equant polyhedral", "ops": [{"set": {"010": 0.9}}]},
    {"code": "E1", "label": "E1", "detail": "elongate [001] 2:1", "text": "elongate along [001], 2:1", "ops": [{"set": {"010": 0.9}}, {"aspect": 2.0}]},
    {"code": "E2", "label": "E2", "detail": "elongate [001] 3.5:1", "text": "elongate along [001], 3.5:1", "ops": [{"set": {"010": 0.9}}, {"aspect": 3.5}]},
]
COLS = [
    {"code": "a", "label": "a", "detail": "{010} {110} {021}", "text": "forms {010}, {110}, {021}",
     "ops": [{"set": {"120": N, "100": N, "101": N, "111": N, "001": N}}]},
    {"code": "b", "label": "b", "detail": "+ {101}", "text": "+ dome {101}", "ops": [{"set": {"120": N, "100": N, "111": N, "001": N}}]},
    {"code": "c", "label": "c", "detail": "+ {111} {001}", "text": "+ dipyramid {111} and basal {001}", "ops": [{"set": {"120": N, "100": N}}]},
    {"code": "d", "label": "d", "detail": "+ {120} {100}", "text": "all common forms incl. {120} and {100}", "ops": []},
]


def spec():
    return grid_spec(
        id=ID, name="Olivine", formula="(Mg,Fe)₂SiO₄", group="Orthosilicates",
        chronometers="Fe–Mg, Ni, Ca diffusion chronometry (magma timescales)",
        system="Orthorhombic", setting="Pbnm (a 4.75 < c 5.98 < b 10.19 Å; Pnma: (hkl) → (klh))",
        lattice=dict(a=4.752, b=10.192, c=5.978), lattice_source="Kirfel et al. (2005)", point_group="mmm",
        forms=FORMS,
        base={"010": 0.9, "110": 1.0, "120": 1.08, "100": 1.12, "021": 1.05, "101": 1.15, "111": 1.12, "001": 1.3},
        rows=ROWS, cols=COLS, default=(2, 2), mono_color="#7d9a3a", view={"tilt": 16, "turn": -30},
        title="Tabular ↔ elongate × form complexity",
        subtitle="Rows run from crystals flattened on (010) to crystals elongated along [001]. Columns add the domes, dipyramid and minor prisms of polyhedral olivine phenocrysts.",
        row_title="Flattening / elongation", col_title="Forms present",
        note=("All indices are in the Pbnm cell, which equals Dana's morphological axes. 8 interfacial angles match Dana (1892) "
              "to within 0.1°. Many diffusion papers use Pnma, where (hkl)<sub>Pbnm</sub> = (klh)<sub>Pnma</sub>. Which forms "
              "dominate follows the standard drawings, and aspect ratios are illustrative. Hopper, skeletal and dendritic "
              "olivine is not convex and is not modelled."),
        about="""
<p>Olivine's external shape records how fast it grew. Slowly cooled phenocrysts are polyhedral, combining {010}, {110},
{021}, {101} and {111}, while faster undercooling gives hopper, skeletal, chain and dendritic crystals (Donaldson 1976;
Faure et al. 2003). Many polyhedral phenocrysts started as dendrites (Welsch et al. 2013, 2014).</p>
<p>3D shape matters directly for <strong>diffusion chronometry</strong>. Fe–Mg diffusion is fastest along [001], and a
random 2D section through a 3D crystal can mislead the timescale estimate (Shea et al. 2015). The polyhedra here are the
3D shapes such sections cut through.</p>""",
        habits=[
            {"name": "Polyhedral phenocryst", "text": "Equant to slightly elongate along [001], mildly flattened on (010); dominated by {010}, {110}, {021} (row Q)."},
            {"name": "Tabular on (010)", "text": "Dana: crystals often flattened parallel to b (rows T1–T2)."},
            {"name": "Prismatic along [001]", "text": "Gem peridot and forsterite: striated prisms with wedge-shaped {021}+{101} terminations (rows E1–E2)."},
            {"name": "Not modelled", "text": "Hopper, skeletal and dendritic crystals from rapid undercooling are not convex."},
        ],
        references=[
            ref("Donaldson, C.H. (1976). An experimental investigation of olivine morphology. <i>Contributions to Mineralogy and Petrology</i> 57, 187–213.",
                "10.1007/BF00405225", "The classic study of olivine morphology versus cooling rate: polyhedral → hopper → chain → dendrite.", ["morphology"]),
            ref("Faure, F., Trolliard, G., Nicollet, C., Montel, J.-M. (2003). A developmental model of olivine morphology as a function of the cooling rate and the degree of undercooling. <i>Contributions to Mineralogy and Petrology</i> 145, 251–263.",
                "10.1007/s00410-003-0449-y", "Morphology as a function of undercooling.", ["morphology"]),
            ref("Welsch, B., Faure, F., Famin, V., Baronnet, A., Bachèlery, P. (2013). Dendritic crystallization: a single process for all the textures of olivine in basalts? <i>Journal of Petrology</i> 54, 539–574.",
                "10.1093/petrology/egs077", "Polyhedral phenocrysts can grow from dendrites.", ["morphology"]),
            ref("Welsch, B., Hammer, J., Hellebrand, E. (2014). Phosphorus zoning reveals dendritic architecture of olivine. <i>Geology</i> 42, 867–870.",
                "10.1130/G35691.1", "Internal growth architecture versus external polyhedral habit.", ["morphology"]),
            ref("Shea, T., Costa, F., Krimer, D., Hammer, J.E. (2015). Accuracy of timescales retrieved from diffusion modeling in olivine: A 3D perspective. <i>American Mineralogist</i> 100, 2026–2042.",
                "10.2138/am-2015-5163", "3D crystal shape, sectioning and anisotropy effects on diffusion timescales. A direct motivation for 3D habit models.", ["chronometry", "geometry"]),
            ref("Costa, F., Dungan, M. (2005). Short time scales of magmatic assimilation from diffusion modeling of multiple elements in olivine. <i>Geology</i> 33, 837–840.",
                "10.1130/G21675.1", "Olivine diffusion chronometry.", ["chronometry"]),
            ref("Dohmen, R., Chakraborty, S. (2007). Fe–Mg diffusion in olivine II: point defect chemistry, change of diffusion mechanisms and a model for calculation of diffusion coefficients in natural olivine. <i>Physics and Chemistry of Minerals</i> 34, 409–430.",
                "10.1007/s00269-007-0158-6", "Anisotropic Fe–Mg diffusion, fastest along [001].", ["diffusion"]),
            ref("Kirfel, A., Lippmann, T., Blaha, P., Schwarz, K., Cox, D.F., Rosso, K.M., Gibbs, G.V. (2005). Electron density distribution and bond critical point properties for forsterite, Mg<sub>2</sub>SiO<sub>4</sub>, determined with synchrotron single crystal X-ray diffraction data. <i>Physics and Chemistry of Minerals</i> 32, 301–313.",
                "10.1007/s00269-005-0468-5", "The Pbnm cell used here.", ["lattice"]),
        ],
    )
