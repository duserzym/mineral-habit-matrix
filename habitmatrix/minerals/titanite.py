"""Titanite: envelope (wedge) habit -> prismatic and tabular habits.

Setting: C2/c structural cell (a = 6.566, b = 8.722, c = 7.069 Å, β = 113.86°; Speer & Gibbs 1976,
a and c swapped from P2₁/a).  Classical forms are given in Des Cloizeaux/Dana's morphological
cell; their C2/c equivalents are
    c{001} -> {001},  n{111}_Dana -> {110},  m{110}_Dana -> {-111},  a{100}_Dana -> {-101}
(conversion (hkl)_D -> (h, k, l - h) for the acute-β Dana cell; checked against Dana's
interfacial angles to within 0.2°).

Rows   : c{001} share of the surface (prismatic on n -> tabular on c).
Columns: m{-111} share of the surface (n-bounded envelope -> prismatic by extension of m).
"""

from ..habit import ABSENT, Crystal, Form, solve_share
from ..lattice import Lattice
from ._common import ref

ID = "titanite"
C_SHARE = [0.15, 0.3, 0.45, 0.6]
M_SHARE = [0.0, 0.12, 0.25, 0.4]


def crystal() -> Crystal:
    return Crystal(
        "titanite",
        Lattice(6.566, 8.722, 7.069, 90, 113.86, 90),
        "2/m",
        [
            Form("110", (1, 1, 0), "n (Dana {111})", "#8a6a2f"),
            Form("001", (0, 0, 1), "c (Dana {001})", "#d8b25a"),
            Form("-111", (-1, 1, 1), "m (Dana {110})", "#5c7a5a"),
        ],
        elongation_axis=None,
    )


def spec() -> dict:
    tt = crystal()
    cells = []
    for i, fc in enumerate(C_SHARE):
        for j, fm in enumerate(M_SHARE):
            d = {"110": 1.0, "001": 0.6, "-111": ABSENT}
            if fm > 0:
                d = solve_share(tt, {**d, "-111": 1.0}, "-111", fm, "110")
            d = solve_share(tt, d, "001", fc, "110")
            cells.append({
                "id": f"C{i + 1}M{j + 1}", "row": i, "col": j, "label": f"C{i + 1}·M{j + 1}",
                "description": (f"c{{001}} ≈ {round(100 * fc)}% of the surface, m{{1̄11}} ≈ {round(100 * fm)}%, "
                                "the rest n{110}. Indices in the C2/c cell; Dana letters in the legend."),
                "default": (i, j) == (1, 0), "distances": d, "t": 0.0,
            })
    return {
        "id": ID, "name": "Titanite", "group": "Accessory chronometers", "crystal": tt, "formula": "CaTiSiO₅",
        "chronometers": "U–Pb, (U–Th)/He, Zr-in-titanite thermometry",
        "system": "Monoclinic", "setting": "C2/c (a↔c of P2₁/a)",
        "lattice_source": "Speer &amp; Gibbs (1976)",
        "mono_color": "#b08a3c",
        "view": {"tilt": 22, "turn": -35},
        "matrix": {
            "title": "Envelope → prismatic → tabular",
            "subtitle": ("The classic wedge or envelope is n{110} with c{001}. Columns grow the m prism, Dana's {110}. "
                         "Rows flatten the crystal on c{001}."),
            "row_title": "c{001} flattening", "col_title": "m{1̄11} development",
            "rows": [{"label": f"C{i + 1}", "detail": f"c ≈ {round(100 * f)}%"} for i, f in enumerate(C_SHARE)],
            "cols": [{"label": f"M{j + 1}", "detail": "n only" if f == 0 else f"m ≈ {round(100 * f)}%"} for j, f in enumerate(M_SHARE)],
            "note": ("No habit typology exists for titanite, so this grid spans the habits Dana (1892) describes. Indices are "
                     "converted from Dana's morphological cell to C2/c. The conversion was checked numerically against Dana's "
                     "angles, but which faces dominate each named habit is only moderately certain. Contact twins on {1̄01} "
                     "are not convex and are not modelled."),
        },
        "about": """
<p>Titanite (sphene) takes its name from its wedge shape. Magmatic titanite is typically an envelope-shaped crystal
flattened on c{001} and bounded by n. Dana (1892) also describes crystals that are prismatic by extension of m, and
tabular crystals. Morphological indices in Dana, the Handbook of Mineralogy and mindat use the Des Cloizeaux cell
(a:b:c = 0.75467 : 1 : 0.85429, β = 60°17′). They must not be mixed with the P2₁/a or C2/c structural cell, so the
generator converts them to C2/c.</p>
<p>In petrochronology the wedge habit, sector zoning and internal textures help separate magmatic from metamorphic or
hydrothermal titanite. Grain size and shape set the diffusion domain for Pb and He.</p>""",
        "habits": [
            {"name": "Wedge / envelope", "text": "Flattened on c{001} and bounded mainly by n, with smaller m, x and a. Typical of magmatic titanite (column M1)."},
            {"name": "Prismatic on m", "text": "Elongated by the m prism (Dana {110}, C2/c {1̄11}) with n and c terminations (columns M3–M4)."},
            {"name": "Tabular on c", "text": "A large c{001} with narrow n and m rims (rows C3–C4)."},
            {"name": "Twins (not modelled)", "text": "Contact and penetration twins on a (Dana {100}, C2/c {1̄01}), and polysynthetic lamellae on Dana {221}."},
        ],
        "references": [
            ref("Kohn, M.J. (2017). Titanite petrochronology. <i>Reviews in Mineralogy and Geochemistry</i> 83, 419–441.",
                "10.2138/rmg.2017.83.13", "Review of titanite U–Pb, trace-element and Zr thermometry petrochronology.", ["review"]),
            ref("Frost, B.R., Chamberlain, K.R., Schumacher, J.C. (2001). Sphene (titanite): phase relations and role as a geochronometer. <i>Chemical Geology</i> 172, 131–148.",
                "10.1016/S0009-2541(00)00240-0", "Phase relations, and igneous wedge-shaped versus metamorphic titanite textures.", ["review"]),
            ref("Paterson, B.A., Stephens, W.E. (1992). Kinetically induced compositional zoning in titanite: implications for accessory-phase/melt partitioning of trace elements. <i>Contributions to Mineralogy and Petrology</i> 109, 373–385.",
                "10.1007/BF00283325", "Sector zoning tied to the growth kinetics of particular faces.", ["morphology"]),
            ref("Piccoli, P., Candela, P., Rivers, M. (2000). Interpreting magmatic processes from accessory phases: titanite—a small-scale recorder of large-scale processes. <i>Transactions of the Royal Society of Edinburgh: Earth Sciences</i> 91, 257–267.",
                "10.1017/S0263593300007422", "Titanite textures and zoning as records of magmatic processes.", ["morphology"]),
            ref("Reiners, P.W., Farley, K.A. (1999). Helium diffusion and (U–Th)/He thermochronometry of titanite. <i>Geochimica et Cosmochimica Acta</i> 63, 3845–3859.",
                "10.1016/S0016-7037(99)00170-2", "Grain-size dependence of He diffusion. The physical grain acts as the diffusion domain.", ["thermochronology", "geometry"]),
            ref("Cherniak, D.J. (1993). Lead diffusion in titanite and preliminary results on the effects of radiation damage on Pb transport. <i>Chemical Geology</i> 110, 177–194.",
                "10.1016/0009-2541(93)90253-F", "Pb diffusion for closure and grain-size modelling.", ["diffusion"]),
            ref("Speer, J.A., Gibbs, G.V. (1976). The crystal structure of synthetic titanite, CaTiOSiO₄, and the domain textures of natural titanites. <i>American Mineralogist</i> 61, 238–247.",
                None, "The cell used here (P2₁/a a = 7.069, b = 8.722, c = 6.566 Å, β = 113.86°, re-labelled to C2/c).", ["lattice"],
                url="http://www.minsocam.org/ammin/AM61/AM61_238.pdf"),
            ref("Dana, E.S. (1892). <i>The System of Mineralogy</i>, 6th ed. Wiley, New York (titanite).",
                None, "The morphological cell, form letters and habit descriptions (wedge, prismatic on m, tabular).", ["morphology"],
                url="https://archive.org/details/systemofmineralo01danarich"),
        ],
        "cells": cells,
    }
