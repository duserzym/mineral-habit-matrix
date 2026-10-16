"""Kyanite, sillimanite, andalusite, staurolite, vesuvianite, cordierite and tourmaline.

Index conversions from Dana (1892) to the structural cells (each checked against Dana's angles):
  kyanite, sillimanite, andalusite, tourmaline: identical settings
  staurolite: Dana's c is doubled -> (h, k, l/2); Dana r(101) = (201)
  cordierite: Dana's a and b swapped -> (k h l)
  vesuvianite: Dana's cell rotated 45° with a·√2 -> h=(hD-kD)/2, k=(hD+kD)/2
"""

from ._common import ref
from ._grid import form, grid_spec

N = None


def aspect_rows(values, prefix="L", word="along c"):
    return [{"code": f"{prefix}{i + 1}", "label": f"{prefix}{i + 1}", "detail": f"{v:g}:1",
             "text": f"aspect {v:g}:1 {word}", "ops": [{"aspect": v}]} for i, v in enumerate(values)]


AL2SIO5_REFS = [
    ref("Pattison, D.R.M. (1992). Stability of andalusite and sillimanite and the Al<sub>2</sub>SiO<sub>5</sub> triple point: constraints from the Ballachulish aureole, Scotland. <i>The Journal of Geology</i> 100, 423–446.",
        "10.1086/629596", "Field-calibrated Al₂SiO₅ triple point, the basis of polymorph thermobarometry.", ["thermobarometry"]),
    ref("Whitney, D.L. (2002). Coexisting andalusite, kyanite, and sillimanite: sequential formation of three Al<sub>2</sub>SiO<sub>5</sub> polymorphs during progressive metamorphism near the triple point, Sivrihisar, Turkey. <i>American Mineralogist</i> 87, 405–416.",
        "10.2138/am-2002-0404", "Textures and crystallization sequence of all three polymorphs.", ["petrology"]),
    ref("Kerrick, D.M. (ed.) (1990). <i>The Al<sub>2</sub>SiO<sub>5</sub> Polymorphs</i>. Reviews in Mineralogy 22.",
        "10.1515/9781501509094", "The standard review of Al₂SiO₅ crystallography, occurrence and phase equilibria.", ["review"]),
]
PORPHYROBLAST_REF = ref(
    "Carlson, W.D. (2011). Porphyroblast crystallization: linking processes, kinetics, and microstructures. <i>International Geology Review</i> 53, 406–445.",
    "10.1080/00206814.2010.496184", "A framework for porphyroblast nucleation and growth.", ["kinetics"])
BURT = ref("Burt, J.B., Ross, N.L., Angel, R.J., Koch, M. (2006). Equations of state and structures of andalusite to 9.8 GPa and sillimanite to 8.5 GPa. <i>American Mineralogist</i> 91, 319–326.",
           "10.2138/am.2006.1875", "The andalusite and sillimanite cells used here.", ["lattice"])
RICE = ref("Rice, A.H.N., Mitchell, J.I. (1991). Porphyroblast textural sector-zoning and matrix displacement. <i>Mineralogical Magazine</i> 55, 379–396.",
           "10.1180/minmag.1991.055.380.08", "Textural sector zoning of chiastolite and staurolite porphyroblasts.", ["morphology"])


def kyanite_spec():
    forms = [
        form("100", (1, 0, 0), "a, front pinacoid (blade face, cleavage)", "#3d6fb6"),
        form("010", (0, 1, 0), "b, side pinacoid", "#6f97cf"),
        form("110", (1, 1, 0), "m, pinacoid", "#9db8e0"),
        form("1-10", (1, -1, 0), "M, pinacoid", "#c3d3ec"),
        form("001", (0, 0, 1), "c, basal pinacoid (parting)", "#24497d"),
    ]
    cols = [{"code": c, "label": c, "detail": f"width:thickness {r}:1", "text": f"blade width:thickness ≈ {r}:1",
             "ops": [{"set": {"100": 1.0 / r}}]} for c, r in [("w1", 1), ("w2", 2), ("w4", 4), ("w8", 8)]]
    return grid_spec(
        id="kyanite", name="Kyanite", formula="Al₂SiO₅", group="Orthosilicates",
        chronometers="Al₂SiO₅ polymorph thermobarometry; inclusion barometry",
        system="Triclinic", setting="P1̄ (same cell as Dana / vom Rath)",
        lattice=dict(a=7.1200, b=7.8479, c=5.5738, alpha=89.974, beta=101.117, gamma=106.0),
        lattice_source="Yang et al. (1997)", point_group="-1",
        forms=forms, base={"100": 0.5, "010": 1.0, "110": 1.02, "1-10": 1.06, "001": 0.3},
        rows=aspect_rows([1.5, 3, 6, 12]), cols=cols, default=(2, 2), mono_color="#4677bd", view={"tilt": 14, "turn": -40},
        title="Blade elongation × flattening on (100)",
        subtitle="Kyanite blades are tabular on a{100} and elongated along [001], with narrow b{010} edges bevelled by the separate pinacoids m{110} and M{11̄0}.",
        row_title="Elongation along c", col_title="Flattening on (100)",
        note=("Seven interfacial angles match Dana (1892) to within 0.5°, for example a∧b = 73.69° against 73°56′. True "
              "terminations are rare: {001} is a parting plane and is used here as an idealized end. Bent blades are not "
              "modelled."),
        about="""
<p>Kyanite is the high-pressure Al₂SiO₅ polymorph, with the familiar blue blades of schists. Being triclinic, it has
only pinacoids, so m{110} and M{11̄0} develop independently, and the blade face a{100} meets b{010} at 73.7°, not 90°. The
three Al₂SiO₅ polymorphs and their triple point anchor metamorphic thermobarometry (Pattison 1992).</p>""",
        habits=[
            {"name": "Bladed porphyroblast", "text": "Thin blades tabular on {100} and elongated along [001] (columns w4–w8)."},
            {"name": "Columnar lath", "text": "a ≈ b, long along [001] (column w1)."},
        ],
        references=[
            ref("Yang, H., Downs, R.T., Finger, L.W., Hazen, R.M., Prewitt, C.T. (1997). Compressibility and crystal structure of kyanite, Al<sub>2</sub>SiO<sub>5</sub>, at high pressure. <i>American Mineralogist</i> 82, 467–474.",
                "10.2138/am-1997-5-604", "The cell used here.", ["lattice"]),
            ref("Carlson, W.D., Pattison, D.R.M., Caddick, M.J. (2015). Beyond the equilibrium paradigm: How consideration of kinetics enhances metamorphic interpretation. <i>American Mineralogist</i> 100, 1659–1667.",
                "10.2138/am-2015-5097", "Porphyroblast nucleation and growth kinetics, and overstepping.", ["kinetics"]),
        ] + AL2SIO5_REFS,
    )


def sillimanite_spec():
    forms = [
        form("110", (1, 1, 0), "m, prism (88.6°)", "#b9a98a"),
        form("100", (1, 0, 0), "a, pinacoid", "#d6c8aa"),
        form("010", (0, 1, 0), "b, pinacoid (cleavage)", "#8f7f62"),
        form("230", (2, 3, 0), "h, prism", "#e7dcc6"),
        form("001", (0, 0, 1), "c, basal (idealized end)", "#6f6047"),
    ]
    cols = [
        {"code": "m", "label": "m", "detail": "{110} only", "text": "square {110} prism", "ops": []},
        {"code": "o", "label": "o", "detail": "m + a + b", "text": "octagonal m + a + b", "ops": [{"set": {"100": 0.86, "010": 0.86}}]},
        {"code": "h", "label": "h", "detail": "m + h + b", "text": "rounded m + h + b prism zone", "ops": [{"set": {"230": 1.0, "010": 0.9}}]},
        {"code": "b", "label": "b", "detail": "(010)-flattened", "text": "flattened on the (010) cleavage", "ops": [{"set": {"010": 0.55}}]},
    ]
    return grid_spec(
        id="sillimanite", name="Sillimanite", formula="Al₂SiO₅", group="Orthosilicates",
        chronometers="Al₂SiO₅ polymorph thermobarometry",
        system="Orthorhombic", setting="Pbnm (same orientation as Dana)",
        lattice=dict(a=7.48388, b=7.6726, c=5.76807), lattice_source="Burt et al. (2006)", point_group="mmm",
        forms=forms, base={"110": 1.0, "001": 0.5}, rows=aspect_rows([3, 6, 12, 25]), cols=cols, default=(1, 1),
        mono_color="#c8b892", view={"tilt": 14, "turn": -30},
        title="Prism zone × elongation",
        subtitle="Long, nearly square {110} prisms (88.6°), striated and rounded by {230}, {100} and {010}. Fibrolite is the extreme of the elongation axis.",
        row_title="Elongation along c", col_title="Prism zone",
        note=("Sillimanite has no documented terminal forms, so the {001} end is an assumed placeholder that closes the solid. "
              "Fibrolite is felted bundles of needles, not a single crystal."),
        about="""
<p>Sillimanite is the high-temperature Al₂SiO₅ polymorph. Its crystals are long square prisms along the Al-octahedral
chain axis [001], often so thin that they form fibrolite. It commonly grows topotactically on andalusite (Vernon 1987).</p>""",
        habits=[
            {"name": "Prismatic", "text": "Long square-section {110} prisms (column m)."},
            {"name": "Fibrolite", "text": "Very high aspect needles (row L4); in rocks these form felted bundles."},
        ],
        references=[
            BURT,
            ref("Vernon, R.H. (1987). Growth and concentration of fibrous sillimanite related to heterogeneous deformation in K-feldspar-sillimanite metapelites. <i>Journal of Metamorphic Geology</i> 5, 51–68.",
                "10.1111/j.1525-1314.1987.tb00369.x", "Fibrolite nucleation and growth microstructures.", ["morphology"]),
            ref("Vernon, R.H. (1987). Oriented growth of sillimanite in andalusite, Placitas-Juan Tabo area, New Mexico, U.S.A. <i>Canadian Journal of Earth Sciences</i> 24, 580–590.",
                "10.1139/e87-057", "Topotactic sillimanite growth on andalusite.", ["morphology"]),
        ] + AL2SIO5_REFS,
    )


def andalusite_spec():
    forms = [
        form("110", (1, 1, 0), "m, prism (89.2°)", "#b06a6a"),
        form("001", (0, 0, 1), "c, basal pinacoid", "#7d3f3f"),
        form("101", (1, 0, 1), "r, dome", "#d39a8e"),
        form("011", (0, 1, 1), "s, dome", "#e6b8ad"),
        form("111", (1, 1, 1), "o, dipyramid", "#f2d6cf"),
    ]
    cap = ["001", "101", "011", "111"]
    cols = [
        {"code": "c", "label": "c", "detail": "{001} only", "text": "flat {001} ends", "ops": []},
        {"code": "s", "label": "cs", "detail": "+ small domes", "text": "{001} with small {101} and {011} domes",
         "ops": [{"share": ["101", 0.12, "001"], "among": cap, "t": 50}, {"share": ["011", 0.12, "001"], "among": cap, "t": 50}]},
        {"code": "d", "label": "d", "detail": "domes dominant", "text": "{101} + {011} domes dominant, small {001}",
         "ops": [{"share": ["101", 0.38, "001"], "among": cap, "t": 50}, {"share": ["011", 0.38, "001"], "among": cap, "t": 50}]},
        {"code": "o", "label": "o", "detail": "+ {111}", "text": "{001} + domes + dipyramid {111}",
         "ops": [{"share": ["101", 0.2, "001"], "among": cap, "t": 50}, {"share": ["011", 0.2, "001"], "among": cap, "t": 50},
                 {"share": ["111", 0.12, "001"], "among": cap, "t": 50, "stage": 0.6}]},
    ]
    return grid_spec(
        id="andalusite", name="Andalusite", formula="Al₂SiO₅", group="Orthosilicates",
        chronometers="Al₂SiO₅ polymorph thermobarometry (contact aureoles)",
        system="Orthorhombic", setting="Pnnm (same as Dana / Des Cloizeaux)",
        lattice=dict(a=7.793, b=7.89734, c=5.55583), lattice_source="Burt et al. (2006)", point_group="mmm",
        forms=forms, base={"110": 1.0, "001": 0.3}, rows=aspect_rows([0.8, 1.5, 3, 6]), cols=cols, default=(2, 0),
        mono_color="#a86a64", view={"tilt": 16, "turn": -30},
        title="Termination × elongation",
        subtitle="Coarse, nearly square {110} prisms (89.2°) with flat {001} ends, sometimes capped by the domes {101} and {011} and the dipyramid {111}.",
        row_title="Elongation along c", col_title="Termination",
        note=("Five interfacial angles match Dana (1892) to within 0.1°, for example m∧r = 65.59° against 65°36′. The dark "
              "cross of chiastolite is an internal pattern of graphite inclusions along the prism diagonals; its outer "
              "shape is the square prism shown here. Dome sizes are set as shares of the termination area."),
        about="""
<p>Andalusite is the low-pressure Al₂SiO₅ polymorph of contact aureoles. Its stout square prisms are close to tetragonal
because a ≈ b. In chiastolite, graphite inclusions swept along the growing prism edges form a dark cross, a record of
displacive porphyroblast growth (Rice &amp; Mitchell 1991).</p>""",
        habits=[
            {"name": "Square prism", "text": "{110} with flat {001} ends (column c)."},
            {"name": "Chiastolite", "text": "The same outer prism, with an internal inclusion cross (not drawn)."},
            {"name": "Terminated", "text": "c with r and s domes and small o (column o)."},
        ],
        references=[BURT, RICE, PORPHYROBLAST_REF] + AL2SIO5_REFS,
    )


def staurolite_spec():
    forms = [
        form("110", (1, 1, 0), "m, prism", "#7a4b2e"),
        form("010", (0, 1, 0), "b, pinacoid", "#a8714a"),
        form("001", (0, 0, 1), "c, basal pinacoid", "#4f2f1c"),
        form("201", (2, 0, 1), "r, pinacoid (Dana {101})", "#c99a74"),
        form("-201", (-2, 0, 1), "r′, pinacoid (pseudo-equivalent)", "#c99a74"),
    ]
    cols = [{"code": c, "label": c, "detail": t, "text": f"{t} cross-section",
             "ops": [{"pair": ["110", "010", f], "mode": "prism"}]}
            for c, f, t in [("m", 1.0, "rhombic {110}"), ("s", 0.8, "small b"), ("h", 0.5, "pseudo-hexagonal, b ≈ m"), ("b", 0.25, "flattened on b")]]
    return grid_spec(
        id="staurolite", name="Staurolite", formula="Fe₂Al₉Si₄O₂₃(OH)", group="Orthosilicates",
        chronometers="Metapelite thermobarometry (index mineral)",
        system="Monoclinic (pseudo-orthorhombic)", setting="C2/m, β ≈ 90.1° (Dana's c is doubled: r(101) → (201))",
        lattice=dict(a=7.8628, b=16.6128, c=5.65004, beta=90.093), lattice_source="Hawthorne et al. (1993), COD 9013738",
        point_group="2/m",
        forms=forms, base={"110": 1.0, "010": 1.0, "001": 0.75, "201": 0.8, "-201": 0.8},
        rows=aspect_rows([1, 2, 3.5, 6]), cols=cols, default=(1, 2), mono_color="#6f442a", view={"tilt": 16, "turn": -30},
        title="Prism section × elongation",
        subtitle="Prismatic along [001]. The {110} prism is truncated by b{010}, which can make the section pseudo-hexagonal, and the crystal is capped by c{001} with r{201} bevels.",
        row_title="Elongation along c", col_title="Prism section",
        note=("Dana's morphological c is twice the structural c, so his r(101) is (201) here. rr′ = 110.34° against "
              "Dana's 110°32′. β is so close to 90° that {201} and {2̄01} are kept at the same distance. The famous "
              "90° and 60° cross twins (on {031} and {231}) are not convex and are not modelled."),
        about="""
<p>Staurolite is the index mineral of medium-grade metapelites (Spear &amp; Cheney 1989). It forms rough prisms of
{110} with {010} and {001}, often flattened on b. Its name comes from its interpenetration cross twins (Hurst et al.
1956), which are out of scope here because they are not single convex crystals.</p>""",
        habits=[
            {"name": "Simple prism", "text": "m + b with c and r ends (columns s–h)."},
            {"name": "Flattened on b", "text": "Tabular parallel to (010) (column b)."},
            {"name": "Cross twins (not modelled)", "text": "Penetration twins on {031} (about 90°) and {231} (about 60°)."},
        ],
        references=[
            ref("Comodi, P., Montagnoli, M., Zanazzi, P.F., Ballaran, T.B. (2002). Isothermal compression of staurolite: A single-crystal study. <i>American Mineralogist</i> 87, 1164–1171.",
                "10.2138/am-2002-8-915", "Structure and a cross-check of the cell.", ["lattice"]),
            ref("Hurst, V.J., Donnay, J.D.H., Donnay, G. (1956). Staurolite twinning. <i>Mineralogical Magazine</i> 31, 145–163.",
                "10.1180/minmag.1956.031.233.04", "Classic analysis of the {031} and {231} cross twins.", ["morphology"]),
            ref("Spear, F.S., Cheney, J.T. (1989). A petrogenetic grid for pelitic schists in the system SiO<sub>2</sub>-Al<sub>2</sub>O<sub>3</sub>-FeO-MgO-K<sub>2</sub>O-H<sub>2</sub>O. <i>Contributions to Mineralogy and Petrology</i> 101, 149–164.",
                "10.1007/BF00375302", "Staurolite stability in the metapelite grid.", ["petrology"]),
            ref("Dutrow, B.L., Holdaway, M.J., Hinton, R.W. (1986). Lithium in staurolite and its petrologic significance. <i>Contributions to Mineralogy and Petrology</i> 94, 496–506.",
                "10.1007/BF00376341", "Staurolite crystal chemistry and stability.", ["petrology"]),
            RICE, PORPHYROBLAST_REF,
            ref("Hawthorne, F.C., Ungaretti, L., Oberti, R., Caucia, F., Callegari, A. (1993). The crystal chemistry of staurolite. I. <i>The Canadian Mineralogist</i> 31, 551–582.",
                None, "The cell used here (COD record).", ["lattice"], url="https://www.crystallography.net/cod/9013738.html"),
        ],
    )


def vesuvianite_spec():
    forms = [
        form("100", (1, 0, 0), "m, prism (Dana {110})", "#6f7f3a"),
        form("110", (1, 1, 0), "a, prism (Dana {100})", "#98a65a"),
        form("001", (0, 0, 1), "c, basal pinacoid", "#4d5a26"),
        form("101", (1, 0, 1), "p, dipyramid (Dana {111})", "#c3c98a"),
        form("301", (3, 0, 1), "t, steep dipyramid (Dana {331})", "#a28b4a"),
    ]
    cap = ["001", "101", "301"]
    rows = [{"code": "P0", "label": "P0", "detail": "no prism", "text": "no prism (low dipyramid)", "ops": [{"set": {"100": N, "110": N}}]}] + \
        [{"code": f"P{i + 1}", "label": f"P{i + 1}", "detail": f"{v:g}:1", "text": f"prismatic, aspect {v:g}:1",
          "ops": [{"aspect": v, "requires": "100"}]} for i, v in enumerate([1.0, 2.0, 4.0])]
    cols = [
        {"code": "c", "label": "c", "detail": "{001} flat", "text": "flat {001} termination", "ops": [{"set": {"001": 0.4}}]},
        {"code": "p", "label": "cp", "detail": "{001} + {101}", "text": "{001} + {101} termination",
         "ops": [{"set": {"001": 0.8, "101": 1.0}}, {"share": ["101", 0.5, "001"], "among": cap, "t": 50, "requires": "100"}]},
        {"code": "q", "label": "p", "detail": "{101} only", "text": "{101} dipyramid termination", "ops": [{"set": {"101": 0.9}}]},
        {"code": "t", "label": "t", "detail": "{301} steep", "text": "steep {301} with {101}", "ops": [{"set": {"301": 0.85, "101": 0.95}}]},
    ]
    return grid_spec(
        id="vesuvianite", name="Vesuvianite", formula="Ca₁₉(Al,Mg,Fe)₁₃(SiO₄)₁₀(Si₂O₇)₄(OH,F,O)₁₀", group="Sorosilicates",
        chronometers="Skarn and rodingite petrology",
        system="Tetragonal", setting="P4/nnc (Dana's cell rotated 45°, a·√2)",
        lattice=dict(a=15.536, b=15.536, c=11.781), lattice_source="Galuskin et al. (2003)", point_group="4/mmm",
        forms=forms, base={"100": 1.0, "110": 1.05}, rows=rows, cols=cols, default=(2, 1),
        skip=((0, 0),),  # no prism + flat {001} alone is not a closed solid
        mono_color="#7d8a44", view={"tilt": 16, "turn": -24},
        title="Prism length × termination",
        subtitle="Square-octagonal prisms of m{100} and a{110}, terminated by flat c{001}, the dipyramid p{101} or the steep t{301}. The top row has no prism, giving the low-pyramidal habit.",
        row_title="Prism development", col_title="Termination",
        note=("Dana's morphological cell is rotated 45° with a multiplied by √2, so his m(110), a(100), p(111) and t(331) are "
              "{100}, {110}, {101} and {301} here. c∧p = 37.17° against 37°13.5′. Low-temperature vesuvianite can have "
              "lower symmetry in growth sectors, but this does not change the idealized shape."),
        about="""
<p>Vesuvianite (idocrase) is a skarn and rodingite mineral. Its square-octagonal prisms are commonly terminated by c
alone or by c and p. Dana also describes low pyramids with no prism, sharp {301} pyramids, and long prisms or whiskers
(Galuskin et al. 2003). Ordering in individual growth sectors lowers its true symmetry (Armbruster &amp; Gnos 2000;
Tanaka et al. 2002).</p>""",
        habits=[
            {"name": "Prismatic, c-terminated", "text": "m + a with flat c and small p (columns c–cp)."},
            {"name": "Low pyramidal", "text": "No prism, {101} ± c (row P0)."},
            {"name": "Sharp pyramidal", "text": "Steep {301} (column t)."},
        ],
        references=[
            ref("Galuskin, E.V., Armbruster, T., Malsy, A., Galuskina, I.O., Sitarz, M. (2003). Morphology, composition and structure of low-temperature P4/nnc high-fluorine vesuvianite whiskers from Polar Yakutia, Russia. <i>The Canadian Mineralogist</i> 41, 843–856.",
                "10.2113/gscanmin.41.4.843", "The cell used here, and the link between morphology and structure.", ["lattice", "morphology"]),
            ref("Armbruster, T., Gnos, E. (2000). P4/n and P4nc long-range ordering in low-temperature vesuvianites. <i>American Mineralogist</i> 85, 563–569.",
                "10.2138/am-2000-0418", "Symmetry lowering relative to P4/nnc.", ["crystallography"]),
            ref("Tanaka, T., Akizuki, M., Kudoh, Y. (2002). Optical properties and crystal structure of triclinic growth sectors in vesuvianite. <i>Mineralogical Magazine</i> 66, 261–274.",
                "10.1180/0026461026620027", "Ordering that depends on the growth sector, i.e. on the face.", ["morphology"]),
        ],
    )


def cordierite_spec():
    forms = [
        form("001", (0, 0, 1), "c, basal pinacoid", "#3c4f8f"),
        form("100", (1, 0, 0), "b (Dana), pinacoid", "#6a7fc0"),
        form("110", (1, 1, 0), "m, prism", "#8b9ed6"),
        form("010", (0, 1, 0), "a (Dana), pinacoid", "#a9b7e2"),
        form("310", (3, 1, 0), "d, prism (Dana {130})", "#c6d0ee"),
        form("111", (1, 1, 1), "r, dipyramid", "#e0c46a"),
        form("201", (2, 0, 1), "p, dome (Dana {021})", "#e9d58e"),
    ]
    rows = aspect_rows([0.3, 0.8, 1.5, 3])
    cols = [
        {"code": "A", "label": "A", "detail": "{100}+{110}", "text": "pseudo-hexagonal prism A = {100}+{110}", "ops": [{"set": {"010": N, "310": N}}]},
        {"code": "AB", "label": "A>B", "detail": "12-sided", "text": "prism A with small prism B = {010}+{310}", "ops": [{"set": {"010": 1.08, "310": 1.08}}]},
        {"code": "AeB", "label": "A=B", "detail": "A ≈ B", "text": "prisms A ≈ B", "ops": [{"set": {"010": 1.02, "310": 1.02}}]},
        {"code": "B", "label": "B", "detail": "{010}+{310}", "text": "pseudo-hexagonal prism B = {010}+{310}", "ops": [{"set": {"100": N, "110": N, "010": 1.0, "310": 1.0}}]},
    ]
    return grid_spec(
        id="cordierite", name="Cordierite", formula="(Mg,Fe)₂Al₄Si₅O₁₈·n(H₂O,CO₂)", group="Ring silicates",
        chronometers="Channel H₂O/CO₂ as a fluid record; low-P metamorphic thermobarometry",
        system="Orthorhombic (pseudo-hexagonal)", setting="Cccm (Dana's a and b swapped: (hkl) → (k h l))",
        lattice=dict(a=17.0568, b=9.7154, c=9.3472), lattice_source="Malcherek et al. (2001)", point_group="mmm",
        forms=forms, base={"100": 1.0, "110": 1.0, "001": 0.3, "111": 0.75, "201": 0.75},
        rows=rows, cols=cols, default=(2, 0), mono_color="#5b6fb4", view={"tilt": 18, "turn": -20},
        title="Pseudo-hexagonal prism × elongation",
        subtitle="Two different orthorhombic prisms both look hexagonal: A = {100}+{110} and B = {010}+{310}, each with faces about 60° apart. Short prisms are capped by c{001} with the pseudo-hexagonal pyramid r{111}+p{201}.",
        row_title="Prism height / width", col_title="Prism set",
        note=("Dana's cell has a and b swapped relative to the structure, so his b(010) cleavage is (100) here. Pyramid angles "
              "match Dana to within 0.1°, but the prism angle is 1.5° off because Miller's 1850s axial ratios are imprecise. "
              "Sector trillings are not modelled."),
        about="""
<p>Cordierite is orthorhombic, but a ≈ √3·b makes it pseudo-hexagonal. That is why crystals look like short hexagonal
prisms, and why cyclic sector trillings with a hexagonal outline are common. Trillings have been read as inversion from
hexagonal indialite or as rapid, overstepped growth (Putnis &amp; Holland 1986; Kitamura &amp; Yamada 1987). Molecules
trapped in its ring channels record metamorphic fluids.</p>""",
        habits=[
            {"name": "Short pseudo-hexagonal prism", "text": "c with prism A or B (rows L1–L2)."},
            {"name": "With dipyramid", "text": "Bevelled by the pseudo-hexagonal r + p pyramid."},
            {"name": "Sector trilling (not modelled)", "text": "A cyclic twin with six sectors."},
        ],
        references=[
            ref("Malcherek, T., Domeneghetti, M.C., Tazzoli, V., Ottolini, L., McCammon, C., Carpenter, M.A. (2001). Structural properties of ferromagnesian cordierites. <i>American Mineralogist</i> 86, 66–79.",
                "10.2138/am-2001-0108", "The cell used here.", ["lattice"]),
            ref("Putnis, A., Holland, T.J.B. (1986). Sector trilling in cordierite and equilibrium overstepping in metamorphism. <i>Contributions to Mineralogy and Petrology</i> 93, 265–272.",
                "10.1007/BF00371328", "Links trilling morphology to overstepped growth.", ["morphology"]),
            ref("Kitamura, M., Yamada, H. (1987). Origin of sector trilling in cordierite in Daimonji hornfels, Kyoto, Japan. <i>Contributions to Mineralogy and Petrology</i> 97, 1–6.",
                "10.1007/BF00375209", "Sector-trilling cordierite in a contact aureole.", ["morphology"]),
            ref("Kitamura, M., Hiroi, Y. (1982). Indialite from Unazuki pelitic schist, Japan, and its transition texture to cordierite. <i>Contributions to Mineralogy and Petrology</i> 80, 110–116.",
                "10.1007/BF00374888", "Hexagonal-to-orthorhombic transition texture, the origin of the pseudo-hexagonal habit.", ["morphology"]),
        ],
    )


def tourmaline_spec():
    forms = [
        form("01-10", (0, 1, -1, 0), "m, trigonal prism", "#1f2a2e"),
        form("11-20", (1, 1, -2, 0), "a, hexagonal prism", "#3f5559"),
        form("10-11", (1, 0, -1, 1), "r, top trigonal pyramid (+c, antilogous)", "#c65b6b"),
        form("02-21", (0, 2, -2, 1), "o, top steep trigonal pyramid", "#e08a95"),
        form("01-1-1", (0, 1, -1, -1), "r, bottom trigonal pyramid (−c, analogous)", "#5f9c74"),
        form("000-1", (0, 0, 0, -1), "c̄, bottom pedion", "#8cc09d"),
    ]
    cols = [{"code": c, "label": c, "detail": t, "text": f"{t} cross-section",
             "ops": [{"pair": ["01-10", "11-20", f], "mode": "prism"}]}
            for c, f, t in [("m", 1.0, "trigonal (m only)"), ("ma", 0.75, "9-sided, m > a"), ("me", 0.5, "m ≈ a"), ("a", 0.0, "hexagonal (a only)")]]
    return grid_spec(
        id="tourmaline", name="Tourmaline", formula="Na(Fe,Mg)₃Al₆(Si₆O₁₈)(BO₃)₃(OH)₃(OH,F)", group="Ring silicates",
        chronometers="B-isotope and sector-zoning thermometry; provenance",
        system="Trigonal", setting="R3m, hexagonal axes (polar point group 3m)",
        lattice=dict(a=15.9443, b=15.9443, c=7.2094, gamma=120), lattice_source="Marschall et al. (2004), dravite", point_group="3m",
        forms=forms, base={"01-10": 1.0, "11-20": 1.0, "10-11": 1.0, "02-21": 1.12, "01-1-1": 1.0, "000-1": 0.9},
        rows=aspect_rows([0.8, 1.5, 4, 10]), cols=cols, default=(1, 1), mono_color="#2c3a3e", view={"tilt": 3, "turn": -20},
        title="Prism section × elongation (hemimorphic)",
        subtitle="Point group 3m is polar: the two ends differ. Here the top (antilogous, +c) is r{101̄1} with steep o{022̄1} and the bottom is r{011̄1̄} with a pedion. The prism runs from the trigonal m{011̄0} to the hexagonal a{112̄0}.",
        row_title="Elongation along c", col_title="Prism section",
        note=("Six interfacial angles match Dana (1892) and Ford–Dana (1922) to within 0.4°, for example c∧r = 27.57° against "
              "27°20′. The polarity convention (antilogous = +c) follows Barton (1969) and van Hinsberg et al. (2006). Which "
              "trigonal prism dominates rests on one statement in Dana (1892); if it is reversed, swap m and m′. Prism faces "
              "are strongly striated along c in real crystals."),
        about="""
<p>Tourmaline is the classic <em>hemimorphic</em> crystal: it has no mirror plane normal to c, so its two ends grow
different faces and accumulate different chemistry. Hourglass sector zoning between the +c and −c pyramids and the
prism faces fractionates major and trace elements and B isotopes (van Hinsberg et al. 2006; van Hinsberg &amp; Marschall
2007). Inter-sector partitioning can even serve as a single-crystal thermometer (van Hinsberg &amp; Schumacher 2007).
The triangular cross-section comes from the trigonal prism {011̄0}.</p>""",
        habits=[
            {"name": "Metamorphic porphyroblast", "text": "Short prism with r at both ends (rows L1–L2)."},
            {"name": "Prismatic, hemimorphic", "text": "Long trigonal or 9-sided prism with different terminations (rows L3–L4)."},
            {"name": "Hexagonal prism", "text": "The a prism alone (column a)."},
        ],
        references=[
            ref("Barton, R. Jr. (1969). Refinement of the crystal structure of buergerite and the absolute orientation of tourmalines. <i>Acta Crystallographica B</i> 25, 1524–1533.",
                "10.1107/S0567740869004286", "Absolute structure and polarity: the basis of the +c/−c convention.", ["crystallography"]),
            ref("van Hinsberg, V.J., Schumacher, J.C., Kearns, S., Mason, P.R.D., Franz, G. (2006). Hourglass sector zoning in metamorphic tourmaline and resultant major and trace-element fractionation. <i>American Mineralogist</i> 91, 717–728.",
                "10.2138/am.2006.1920", "Polarity-dependent sector chemistry on the r, m and a growth faces.", ["morphology", "geochemistry"]),
            ref("van Hinsberg, V.J., Schumacher, J.C. (2007). Intersector element partitioning in tourmaline: a potentially powerful single crystal thermometer. <i>Contributions to Mineralogy and Petrology</i> 153, 289–301.",
                "10.1007/s00410-006-0147-7", "A sector-zoning thermometer.", ["thermometry"]),
            ref("van Hinsberg, V.J., Marschall, H.R. (2007). Boron isotope and light element sector zoning in tourmaline: Implications for the formation of B-isotopic signatures. <i>Chemical Geology</i> 238, 141–148.",
                "10.1016/j.chemgeo.2006.11.002", "B-isotope sector effects, important for B-isotope petrochronology.", ["geochemistry"]),
            ref("Henry, D.J., Dutrow, B.L. (1996). Metamorphic tourmaline and its petrologic applications. In: Boron. <i>Reviews in Mineralogy</i> 33, 503–558.",
                "10.1515/9781501509223-012", "Polar overgrowths and habit of metamorphic tourmaline.", ["review"]),
            ref("Henry, D.J., Dutrow, B.L. (2018). Tourmaline studies through time: contributions to scientific advancements. <i>Journal of Geosciences</i> 63, 77–98.",
                "10.3190/jgeosci.255", "Polarity and the preferences of +c and −c pyramids.", ["review"]),
            ref("Marschall, H.R., Jiang, S.-Y. (2011). Tourmaline isotopes: no element left behind. <i>Elements</i> 7, 313–319.",
                "10.2113/gselements.7.5.313", "Isotope applications.", ["geochemistry"]),
            ref("Henry, D.J., Novák, M., Hawthorne, F.C., Ertl, A., Dutrow, B.L., Uher, P., Pezzotta, F. (2011). Nomenclature of the tourmaline-supergroup minerals. <i>American Mineralogist</i> 96, 895–913.",
                "10.2138/am.2011.3636", "Current nomenclature and formula.", ["review"]),
            ref("Marschall, H.R., Ertl, A., Hughes, J.M., McCammon, C. (2004). Metamorphic Na- and OH-rich disordered dravite with tetrahedral boron, associated with omphacite, from Syros, Greece. <i>European Journal of Mineralogy</i> 16, 817–823.",
                "10.1127/0935-1221/2004/0016-0817", "The dravite cell used here.", ["lattice"]),
        ],
    )
