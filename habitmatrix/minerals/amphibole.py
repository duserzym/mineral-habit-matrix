"""Amphibole (calcic, hornblende): prism cross-section x elongation.

Forms (C2/m, b-unique): prism {110} (the 56°/124° cleavage prism), side pinacoid {010},
terminations {011} and {-101}.

Rows   : length/width aspect (stubby hornblende -> acicular actinolite).
Columns: {010} share of the prism cross-section ({110} rhomb -> pseudo-hexagon -> {010}-rich).
"""

from ..habit import Crystal, Form
from ..lattice import Lattice
from ._common import ref, frac_text, prism_then_cap

ID = "amphibole"
SIDE = [0.0, 0.2, 0.35, 0.5]   # {010} share of prism perimeter
ASPECTS = [1.5, 2.5, 4.0, 7.0]


def crystal() -> Crystal:
    return Crystal(
        "amphibole",
        Lattice(9.887, 18.174, 5.308, 90, 104.97, 90),
        "2/m",
        [
            Form("110", (1, 1, 0), "prism m", "#2f4a3a"),
            Form("010", (0, 1, 0), "side pinacoid b", "#5f7f4f"),
            Form("011", (0, 1, 1), "termination r", "#a7a05a"),
            Form("-101", (-1, 0, 1), "termination", "#8c6d4a"),
        ],
        elongation_axis=(0, 0, 1),
    )


def spec() -> dict:
    am = crystal()
    base = {"110": 1.0, "010": 1.0, "011": 1.0, "-101": 1.0}
    cells = []
    for i, asp in enumerate(ASPECTS):
        for j, fs in enumerate(SIDE):
            d, t = prism_then_cap(am, base, ("110", "010", 1 - fs), None, asp)
            cells.append({
                "id": f"A{asp:g}_S{j + 1}", "row": i, "col": j, "label": f"L{i + 1}·S{j + 1}", "sub": f"{asp:g}:1",
                "description": f"Prism: {frac_text('{110}', '{010}', 1 - fs)}. Aspect ratio {asp:g}:1 along c.",
                "default": (i, j) == (1, 2), "distances": d, "t": t,
            })
    return {
        "id": ID, "name": "Amphibole", "group": "Chain silicates", "crystal": am, "formula": "Ca₂(Mg,Fe)₄Al(Si₇Al)O₂₂(OH)₂",
        "chronometers": "⁴⁰Ar/³⁹Ar, K–Ar",
        "system": "Monoclinic", "setting": "C2/m (hornblende)",
        "lattice_source": "Handbook of Mineralogy (magnesiohornblende)",
        "mono_color": "#3c5446",
        "matrix": {
            "title": "Prism cross-section × elongation",
            "subtitle": "The prism is the {110} cleavage prism plus the side pinacoid {010}, with {011} and {1̄01} terminations. Rows run from stubby to acicular habits.",
            "row_title": "Aspect ratio (L/W)", "col_title": "Prism cross-section",
            "rows": [{"label": f"L{i + 1}", "detail": f"{a:g}:1"} for i, a in enumerate(ASPECTS)],
            "cols": [{"label": f"S{j + 1}", "detail": frac_text("{110}", "{010}", 1 - f)} for j, f in enumerate(SIDE)],
            "note": "",
        },
        "about": ABOUT,
        "habits": HABITS,
        "references": REFERENCES,
        "cells": cells,
    }


ABOUT = """
<p>Hornblende is a key <sup>40</sup>Ar/<sup>39</sup>Ar thermochronometer. Its habit is a prism of the {110} cleavage
form, giving the 56°/124° cleavage angles, combined with the side pinacoid {010} into a pseudo-hexagonal cross-section.
It is terminated by r{011} and p{1̄01}. Dana's (1892) p{101} uses the acute-β convention and is {1̄01} in the modern
C2/m cell. Diffusion models treat the grain as a cylinder with the grain radius as the diffusion length (Dodson's
geometry factor A = 27 for a cylinder). Villa (1998) argues that microstructure, not geometry alone, controls
closure. No morphology–petrogenesis typology for amphibole has been published.</p>
"""

HABITS = [
    {"name": "Common hornblende", "text": "An m{110} + b{010} prism with a pseudo-hexagonal cross-section, terminated by r{011} (columns S2–S4)."},
    {"name": "Pseudo-rhombohedral ends", "text": "r{011} and p{1̄01} about equally developed."},
    {"name": "Short-prismatic", "text": "m + b + r, sometimes with a{100} (top rows)."},
    {"name": "Acicular / fibrous", "text": "Actinolite and tremolite with very long m (bottom row)."},
]

REFERENCES = [
    ref("Hawthorne, F.C., Oberti, R. (2007). Amphiboles: crystal chemistry. <i>Reviews in Mineralogy and Geochemistry</i> 67, 1–54.",
        "10.2138/rmg.2007.67.1", "Amphibole structure and crystal chemistry.", ["review"]),
    ref("Hawthorne, F.C. et al. (2012). Nomenclature of the amphibole supergroup. <i>American Mineralogist</i> 97, 2031–2048.",
        "10.2138/am.2012.4276", "Amphibole nomenclature.", ["review"]),
    ref("Harrison, T.M. (1981). Diffusion of <sup>40</sup>Ar in hornblende. <i>Contributions to Mineralogy and Petrology</i> 78, 324–331.",
        "10.1007/BF00398927", "Uses the grain radius as the diffusion domain, in cylindrical geometry.", ["thermochronology", "geometry"]),
    ref("Baldwin, S.L., Harrison, T.M., FitzGerald, J.D. (1990). Diffusion of <sup>40</sup>Ar in metamorphic hornblende. <i>Contributions to Mineralogy and Petrology</i> 105, 691–703.",
        "10.1007/BF00306534", "Ar diffusion in metamorphic hornblende.", ["thermochronology"]),
    ref("Villa, I.M. (1998). Isotopic closure. <i>Terra Nova</i> 10, 42–47.",
        "10.1046/j.1365-3121.1998.00156.x", "Argues that microstructure, not grain geometry alone, sets isotopic closure.", ["thermochronology"]),
    ref("Dodson, M.H. (1973). Closure temperature in cooling geochronological and petrological systems. <i>Contributions to Mineralogy and Petrology</i> 40, 259–274.",
        "10.1007/BF00373790", "Geometry factors A: sphere 55, cylinder 27, plane sheet 8.7. Applies to every mineral on this site.", ["thermochronology", "geometry"]),
]
