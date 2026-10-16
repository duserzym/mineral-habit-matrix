"""Nepheline (P6₃, polar), leucite (cubic pseudo-cell) and sodalite (P4̄3n)."""

from ._common import ref
from ._grid import form, grid_spec

N = None


def nepheline_spec():
    forms = [
        form("10-10", (1, 0, -1, 0), "m, hexagonal prism", "#d9d2c3"),
        form("11-20", (1, 1, -2, 0), "a, second-order prism", "#b9b09d"),
        form("0001", (0, 0, 0, 1), "c, top pedion", "#8f8676"),
        form("000-1", (0, 0, 0, -1), "c̄, bottom pedion", "#8f8676"),
        form("10-11", (1, 0, -1, 1), "p, top pyramid", "#efe8d8"),
        form("10-1-1", (1, 0, -1, -1), "p̄, bottom pyramid", "#efe8d8"),
    ]
    rows = [{"code": f"{i + 1}", "label": f"C{i + 1}", "detail": t, "text": f"{t}, d(c)/d(m) = {r}",
             "ops": [{"set": {"0001": r, "000-1": r}}]}
            for i, (r, t) in enumerate([(0.3, "tabular"), (0.6, "short"), (1.0, "equant"), (1.6, "prismatic"), (2.5, "long-prismatic")])]

    def pyramids(d):
        dp = 0.85 * (0.695 * d["10-10"] + 0.719 * d["0001"])
        return {**d, "10-11": dp, "10-1-1": dp}

    cols = [
        {"code": "a", "label": "6", "detail": "hexagonal", "text": "six-sided prism", "ops": []},
        {"code": "b", "label": "12a", "detail": "a{112̄0} small", "text": "twelve-sided prism, a small", "ops": [{"set": {"11-20": 1.08}}]},
        {"code": "c", "label": "12", "detail": "a ≈ m", "text": "twelve-sided prism, a ≈ m", "ops": [{"set": {"11-20": 1.02}}]},
        {"code": "d", "label": "12p", "detail": "+ p{101̄1}", "text": "twelve-sided prism with pyramid-bevelled summits", "ops": [{"set": {"11-20": 1.02}}, {"fn": pyramids}]},
    ]
    return grid_spec(
        id="nepheline", name="Nepheline", formula="(Na,K)AlSiO₄", group="Framework silicates",
        chronometers="Composition as a crystallization thermometer",
        system="Hexagonal", setting="P6₃ (polar point group 6)",
        lattice=dict(a=9.9995, b=9.9995, c=8.3766, gamma=120), lattice_source="Gatta &amp; Angel (2007)", point_group="6",
        forms=forms, base={"10-10": 1.0}, rows=rows, cols=cols, default=(2, 0), mono_color="#d6cfbf",
        view={"tilt": 18, "turn": -20},
        title="Prism length × prism modification",
        subtitle="Stout six- or twelve-sided prisms with flat {0001} summits. Point group 6 is polar, so the top and bottom pedions and pyramids are separate forms; here they are kept equal, because visible hemimorphism is rare.",
        row_title="Aspect d(c)/d(m)", col_title="Prism / summit",
        note=("Six interfacial angles match Dana (1892) to within 0.12°, for example c∧p = 44.05° against 44°5′. Natural "
              "crystals are often poorly formed."),
        about="""
<p>Nepheline is the main feldspathoid of silica-undersaturated alkaline rocks. Its habit is simple: short six- or
twelve-sided prisms ({101̄0} ± {112̄0}) capped by a dominant basal face, sometimes bevelled by the pyramid {101̄1}.
Nepheline composition has long been used as a crystallization-temperature indicator (Hamilton 1961).</p>""",
        habits=[
            {"name": "Stout prism", "text": "Hexagonal prism with plane summits (column 6)."},
            {"name": "Twelve-sided prism", "text": "m + a prisms (columns 12a–12)."},
            {"name": "Modified summits", "text": "Pyramid bevels on the summit edges (column 12p)."},
        ],
        references=[
            ref("Gatta, G.D., Angel, R.J. (2007). Elastic behavior and pressure-induced structural evolution of nepheline: implications for the nature of the modulated superstructure. <i>American Mineralogist</i> 92, 1446–1455.",
                "10.2138/am.2007.2501", "The cell used here.", ["lattice"]),
            ref("Tait, K.T., Sokolova, E., Hawthorne, F.C., Khomyakov, A.P. (2003). The crystal chemistry of nepheline. <i>The Canadian Mineralogist</i> 41, 61–70.",
                "10.2113/gscanmin.41.1.61", "P6₃ structure and crystal chemistry.", ["lattice"]),
            ref("Hamilton, D.L. (1961). Nephelines as crystallization temperature indicators. <i>The Journal of Geology</i> 69, 321–329.",
                "10.1086/626745", "Nepheline composition as a thermometer.", ["thermometry"]),
        ],
    )


def leucite_spec():
    forms = [
        form("211", (2, 1, 1), "n, icositetrahedron (trapezohedron)", "#ece6dc"),
        form("100", (1, 0, 0), "a, cube", "#c8bca8"),
        form("110", (1, 1, 0), "d, rhombic dodecahedron", "#a99c86"),
    ]
    rows = [{"code": c, "label": c, "detail": t, "text": f"cube {t}", "ops": [{"set": {"100": r}}]}
            for c, r, t in [("A0", N, "absent"), ("A1", 1.18, "d(a)/d(n) 1.18"), ("A2", 1.12, "1.12"), ("A3", 1.06, "1.06")]]
    cols = [{"code": c, "label": c, "detail": t, "text": f"dodecahedron {t}", "ops": [{"set": {"110": r}}]}
            for c, r, t in [("d0", N, "absent"), ("d1", 1.10, "d(d)/d(n) 1.10"), ("d2", 1.04, "1.04"), ("d3", 0.98, "0.98")]]
    return grid_spec(
        id="leucite", name="Leucite", formula="KAlSi₂O₆", group="Framework silicates",
        chronometers="⁴⁰Ar/³⁹Ar (K-rich volcanic rocks); crystal size distributions",
        system="Tetragonal (pseudocubic)", setting="rendered in the cubic Ia3̄d pseudo-cell (true room-T cell I4₁/a)",
        lattice=dict(a=13.53, b=13.53, c=13.53), lattice_source="Peacor (1968), cubic at 635 °C", point_group="m-3m",
        forms=forms, base={"211": 1.0}, rows=rows, cols=cols, elongation_axis=None, default=(0, 0),
        mono_color="#e6dfd2", view={"tilt": 20, "turn": -28},
        title="Icositetrahedron with cube and dodecahedron",
        subtitle="Leucite grows as cubic leucite and on cooling inverts to twinned tetragonal domains that keep the cubic {211} shape. The matrix is a truncation series around that icositetrahedron.",
        row_title="Cube {100}", col_title="Dodecahedron {110}",
        note=("Rendered with cubic symmetry because twinned natural crystals keep the cubic external shape. Using the true "
              "tetragonal room-temperature cell would split {211} into three forms whose angles differ by up to 0.8°. "
              "Groundmass leucite is often rounded."),
        about="""
<p>Leucite is the classic example of a <em>paramorph</em>: it crystallizes as cubic leucite above about 600–690 °C, then
inverts to finely twinned tetragonal domains while keeping its 24-faced icositetrahedral {211} shape. Leucite
textures and size distributions record magmatic processes before eruptions (Shea et al. 2009).</p>""",
        habits=[
            {"name": "Icositetrahedron", "text": "{211} alone, the Vesuvius type (cell A0·d0)."},
            {"name": "With subordinate a and d", "text": "Small cube and dodecahedron truncations."},
        ],
        references=[
            ref("Peacor, D.R. (1968). A high temperature single crystal diffractometer study of leucite, (K,Na)AlSi<sub>2</sub>O<sub>6</sub>. <i>Zeitschrift für Kristallographie</i> 127, 213–224.",
                "10.1524/zkri.1968.127.16.213", "The cubic high-temperature cell.", ["lattice"]),
            ref("Mazzi, F., Galli, E., Gottardi, G. (1976). The crystal structure of tetragonal leucite. <i>American Mineralogist</i> 61, 108–115.",
                None, "The room-temperature I4₁/a structure.", ["lattice"], url="http://www.minsocam.org/ammin/AM61/AM61_108.pdf"),
            ref("Palmer, D.C., Dove, M.T., Ibberson, R.M., Powell, B.M. (1997). Structural behavior, crystal chemistry, and phase transitions in substituted leucite: high-resolution neutron powder diffraction studies. <i>American Mineralogist</i> 82, 16–29.",
                "10.2138/am-1997-1-203", "The cubic–tetragonal transition behind the pseudocubic twinning.", ["crystallography"]),
            ref("Shea, T., Larsen, J.F., Gurioli, L., Hammer, J.E., Houghton, B.F., Cioni, R. (2009). Leucite crystals: surviving witnesses of magmatic processes preceding the 79AD eruption at Vesuvius, Italy. <i>Earth and Planetary Science Letters</i> 281, 88–98.",
                "10.1016/j.epsl.2009.02.014", "Leucite textures and crystal size distributions as records of magmatic timescales.", ["geometry"]),
        ],
    )


def sodalite_spec():
    forms = [
        form("110", (1, 1, 0), "d, rhombic dodecahedron", "#3f5fae"),
        form("100", (1, 0, 0), "a, cube", "#7f97cf"),
        form("111", (1, 1, 1), "o, tetrahedron", "#b9c7ea"),
    ]
    rows = [{"code": c, "label": c, "detail": t, "text": f"cube {t}", "ops": [{"set": {"100": r}}]}
            for c, r, t in [("A0", N, "absent"), ("A1", 1.3, "d(a)/d(d) 1.3"), ("A2", 1.15, "1.15"), ("A3", 1.05, "1.05")]]
    cols = [{"code": c, "label": c, "detail": t, "text": f"tetrahedron {t}", "ops": [{"set": {"111": r}}]}
            for c, r, t in [("o0", N, "absent"), ("o1", 1.15, "d(o)/d(d) 1.15"), ("o2", 1.05, "1.05"), ("o3", 0.95, "0.95")]]
    return grid_spec(
        id="sodalite", name="Sodalite", formula="Na₈(Al₆Si₆O₂₄)Cl₂", group="Framework silicates",
        chronometers="—", system="Cubic", setting="P4̄3n (point group 4̄3m, no inversion)",
        lattice=dict(a=8.880679, b=8.880679, c=8.880679), lattice_source="Antao et al. (2008)", point_group="-43m",
        forms=forms, base={"110": 1.0}, rows=rows, cols=cols, elongation_axis=None, default=(0, 0),
        mono_color="#4a68b3", view={"tilt": 20, "turn": -28},
        title="Dodecahedron with cube and tetrahedron",
        subtitle="Point group 4̄3m has no inversion, so {111} is a tetrahedron that truncates only alternate three-fold corners of the dodecahedron.",
        row_title="Cube {100}", col_title="Tetrahedron {111}",
        note=("Which tetrahedron is 'positive' is not fixed by the morphological literature. Euhedral sodalite is rare; the "
              "common pseudohexagonal prisms elongated along [111] are twins and are not modelled."),
        about="""
<p>Sodalite is a cage-structured feldspathoid of alkaline rocks. Its rare euhedral crystals are rhombic dodecahedra.
It is included here mainly as a teaching example of a cubic crystal without a centre of symmetry: its tetrahedron
faces truncate only half of the dodecahedron's three-fold corners.</p>""",
        habits=[{"name": "Dodecahedral", "text": "{110} alone (cell A0·o0)."}, {"name": "With cube or tetrahedron", "text": "Rare subordinate faces."}],
        references=[
            ref("Hassan, I., Grundy, H.D. (1984). The crystal structures of sodalite-group minerals. <i>Acta Crystallographica B</i> 40, 6–13.",
                "10.1107/S0108768184001683", "P4̄3n structure of sodalite-group minerals.", ["lattice"]),
            ref("Antao, S.M., Hassan, I., Wang, J., Lee, P.L., Toby, B.H. (2008). State-of-the-art high-resolution powder X-ray diffraction (HRPXRD) illustrated with Rietveld structure refinement of quartz, sodalite, tremolite, and meionite. <i>The Canadian Mineralogist</i> 46, 1501–1509.",
                "10.3749/canmin.46.5.1501", "The cell used here.", ["lattice"]),
            ref("Hassan, I., Antao, S.M., Parise, J.B. (2004). Sodalite: high-temperature structures obtained from synchrotron radiation and Rietveld refinements. <i>American Mineralogist</i> 89, 359–364.",
                "10.2138/am-2004-2-315", "Thermal behaviour of the framework.", ["lattice"]),
        ],
    )
