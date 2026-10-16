"""Mica (biotite, 1M polytype): pseudo-hexagonal plates.

Forms (C2/m): basal pinacoid {001}, prism {110}, side pinacoid {010}.  Because β ≠ 90°
the prism faces are parallel to c, which is inclined ~10° to the normal of (001), so
the edges of the plate are slightly bevelled, as they are in real 1M micas.

Rows   : plate thickness / width (thick books -> thin flakes).
Columns: {010} share of the plate outline ({110} rhomb -> pseudo-hexagon).
"""

from ..habit import Crystal, Form
from ..lattice import Lattice
from ._common import ref, frac_text, prism_then_cap

ID = "mica"
SIDE = [0.0, 0.2, 0.333, 0.45]
THICK = [0.6, 0.3, 0.15, 0.06]  # thickness / width along the c axis


def crystal() -> Crystal:
    return Crystal(
        "mica",
        Lattice(9.23 / 3**0.5, 9.23, 10.17),
        "mmm",
        [
            Form("001", (0, 0, 1), "basal pinacoid c", "#3b2d22"),
            Form("110", (1, 1, 0), "prism", "#7a5a3a"),
            Form("010", (0, 1, 0), "side pinacoid b", "#a98458"),
        ],
        elongation_axis=(0, 0, 1),
        measure_plane=(0, 0, 1),
    )


def spec() -> dict:
    mi = crystal()
    base = {"001": 0.02, "110": 1.0, "010": 1.0}
    cells = []
    for i, th in enumerate(THICK):
        for j, fs in enumerate(SIDE):
            d, t = prism_then_cap(mi, base, ("110", "010", 1 - fs), None, th)
            cells.append({
                "id": f"T{i + 1}_S{j + 1}", "row": i, "col": j, "label": f"T{i + 1}·S{j + 1}", "sub": f"1:{1 / th:.0f}",
                "description": f"Outline: {frac_text('{110}', '{010}', 1 - fs)}. Thickness:width ≈ 1:{1 / th:.1f}.",
                "default": (i, j) == (1, 2), "distances": d, "t": t,
            })
    return {
        "id": ID, "name": "Mica", "crystal": mi, "formula": "K(Mg,Fe)₃AlSi₃O₁₀(OH)₂",
        "chronometers": "⁴⁰Ar/³⁹Ar, K–Ar, Rb–Sr",
        "system": "Monoclinic", "setting": "orthohexagonal pseudo-cell (a = b/√3, β = 90°)",
        "lattice_source": "orthohexagonal pseudo-cell from biotite-1M (Handbook of Mineralogy)",
        "mono_color": "#4a3628",
        "view": {"tilt": 38, "turn": -20},
        "matrix": {
            "title": "Plate outline × thickness",
            "subtitle": "Basal {001} plates bounded by {110} and {010}. Rows run from thick books to thin flakes.",
            "row_title": "Thickness : width", "col_title": "Plate outline",
            "rows": [{"label": f"T{i + 1}", "detail": f"1:{1 / t:.0f}"} for i, t in enumerate(THICK)],
            "cols": [{"label": f"S{j + 1}", "detail": frac_text("{110}", "{010}", 1 - f)} for j, f in enumerate(SIDE)],
            "note": "",
        },
        "about": ABOUT,
        "habits": HABITS,
        "references": REFERENCES,
        "cells": cells,
    }


ABOUT = """
<p>Biotite and muscovite are workhorse <sup>40</sup>Ar/<sup>39</sup>Ar and Rb–Sr thermochronometers. Their habit is a
pseudo-hexagonal plate: a dominant basal pinacoid c{001} bounded by b{010} and m{110}. Muscovite can be a rhombic
plate of c + m only. The plate radius is generally taken as the Ar diffusion domain, modelled as a cylinder
(Hames &amp; Bowring 1994; Harrison et al. 2009).</p>
<p>The true 1M cell (C2/m, β ≈ 100°) puts {110} at an angle to (001). For rendering, the plates here use an
orthohexagonal pseudo-cell instead: a = b/√3, β = 90°, c = 10.17 Å, with point group mmm. This gives right
pseudo-hexagonal prisms, which is a modelling choice.</p>
"""

HABITS = [
    {"name": "Pseudo-hexagonal plate", "text": "c ≫ b and m (column S3 is close to a regular hexagon)."},
    {"name": "Book", "text": "Thick tabular or short-prismatic, with c comparable to b and m (top row)."},
    {"name": "Rhombic plate", "text": "c + m only, typical of muscovite (column S1)."},
    {"name": "Not modelled", "text": "Tapering prismatic phlogopite with steep pyramids (their indices are uncertain) and mica-law twins."},
]

REFERENCES = [
    ref("Brigatti, M.F., Guggenheim, S. (2002). Mica crystal chemistry and the influence of pressure, temperature, and solid solution on atomistic models. <i>Reviews in Mineralogy and Geochemistry</i> 46, 1–97.",
        "10.2138/rmg.2002.46.01", "Mica crystal chemistry.", ["review"]),
    ref("Hames, W.E., Bowring, S.A. (1994). An empirical evaluation of the argon diffusion geometry in muscovite. <i>Earth and Planetary Science Letters</i> 124, 161–169.",
        "10.1016/0012-821X(94)00079-4", "Shows the Ar diffusion domain is approximately the physical grain.", ["thermochronology", "geometry"]),
    ref("Harrison, T.M., Célérier, J., Aikman, A.B., Hermann, J., Heizler, M.T. (2009). Diffusion of <sup>40</sup>Ar in muscovite. <i>Geochimica et Cosmochimica Acta</i> 73, 1039–1051.",
        "10.1016/j.gca.2008.09.038", "Ar diffusion in muscovite using cylindrical geometry.", ["thermochronology", "geometry"]),
    ref("Harrison, T.M., Duncan, I., McDougall, I. (1985). Diffusion of <sup>40</sup>Ar in biotite: temperature, pressure and compositional effects. <i>Geochimica et Cosmochimica Acta</i> 49, 2461–2468.",
        "10.1016/0016-7037(85)90246-7", "Ar diffusion in biotite.", ["thermochronology"]),
    ref("Grove, M., Harrison, T.M. (1996). <sup>40</sup>Ar* diffusion in Fe-rich biotite. <i>American Mineralogist</i> 81, 940–951.",
        "10.2138/am-1996-7-816", "Composition dependence of Ar diffusion in biotite.", ["thermochronology"]),
    ref("Kirschner, D.L., Cosca, M.A., Masson, H., Hunziker, J.C. (1996). Staircase <sup>40</sup>Ar/<sup>39</sup>Ar spectra of fine-grained white mica: timing and duration of deformation and empirical constraints on argon diffusion. <i>Geology</i> 24, 747–750.",
        "10.1130/0091-7613(1996)024<0747:SAASOF>2.3.CO;2", "Grain size as the diffusion domain in fine white mica.", ["thermochronology", "geometry"]),
    ref("Lovera, O.M., Richter, F.M., Harrison, T.M. (1989). The <sup>40</sup>Ar/<sup>39</sup>Ar thermochronometry for slowly cooled samples having a distribution of diffusion domain sizes. <i>Journal of Geophysical Research</i> 94, 17917–17935.",
        "10.1029/JB094iB12p17917", "The multi-domain diffusion (MDD) model.", ["thermochronology"]),
]
