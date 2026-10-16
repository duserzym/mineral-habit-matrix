# Mineral Habit Matrix

**Live site:** https://duserzym.github.io/mineral-habit-matrix/

This repo generates grids ("habit matrices") of idealized 3D crystal geometries for petrochronometer and
thermochronometer minerals. Zircon follows the Pupin (1980) typology. The other minerals use habit
series taken from the morphology and grain-geometry literature that is cited on the site.

| Mineral | Matrix | Cells | Chronometers |
|---|---|---|---|
| Zircon | Pupin (1980) typology, I.A × I.T (64 subtypes) | 64 | U–Pb, (U–Th)/He, FT, Lu–Hf |
| Xenotime | {100}/{110} prism × elongation, {101} dipyramid | 12 | U–Th–Pb |
| Apatite | termination ({0001} ↔ {10-11}) × elongation | 20 | (U–Th)/He, FT, U–Pb |
| Monazite | {100} tabularity × elongation along b | 16 | U–Th–Pb, (U–Th)/He |
| Titanite | envelope (n{110}+c{001}) → m{-111} prismatic × {001} tabular (C2/c) | 16 | U–Pb, (U–Th)/He |
| Rutile | Pupin-style {110}/{100} prism × {101}/{111} termination | 16 | U–Pb, Zr-in-rutile |
| Garnet | {110} ↔ {211} × {321} modifier | 15 | Sm–Nd, Lu–Hf |
| Amphibole | {110}/{010} prism × elongation | 16 | ⁴⁰Ar/³⁹Ar |
| Mica | {110}/{010} plate outline × thickness | 16 | ⁴⁰Ar/³⁹Ar, Rb–Sr |
| Magnetite | octahedron {111} ↔ dodecahedron {110} × {100}/{311} modifier | 15 | (U–Th)/He, paleomagnetism |
| Hematite | rhombohedral → specular plates × edge forms | 12 | (U–Th)/He, paleomagnetism |

Every mineral page lists its literature: typology and morphology papers, plus the grain-geometry papers
used in α-ejection (F<sub>T</sub>) and diffusion-domain modelling. `scripts/check_dois.py` checks every DOI
against Crossref.

Click any crystal to open an inspector with an orbit view, face-area shares, metrics and downloads. The
**Learn** tab rebuilds any crystal step by step: unit cell, reciprocal-lattice normals, symmetry, half-space
cuts, relative development (with live sliders) and normalization. It runs on a small JavaScript half-space
clipper (`site/geom.js`) that reproduces all of the Python-generated geometries.

Every habit is built from first principles:

1. **Lattice → face normals.** Each face normal comes from the reciprocal lattice, `n = h a* + k b* + l c*`, so the
   lattice parameters (a, b, c, α, β, γ) set the interfacial angles.
2. **Symmetry.** Each form {hkl} is expanded to all of its faces with the mineral's point group.
3. **Wulff / half-space construction.** The crystal is the convex polyhedron `n·x ≤ d`. Each form has one
   central distance `d`.
4. **Relative development → distances.** Typologies describe face development (for example Pupin's {100}:{110} prism
   and {101}:{211} pyramid ratios). These ratios are converted to perimeter or area fractions, and the
   distances are solved by bisection. Elongation translates the terminations rigidly along the c-axis.
5. **Export.** Every crystal is normalized to unit volume (1 mm³) because grain size is not modelled. Each one is
   written as a binary **STL** and as an exact planar B-rep **STEP** (AP214) file.

## Layout

```
habitmatrix/            Python generator (numpy + scipy only)
  lattice.py            lattices, reciprocal lattices, Miller(-Bravais) indices, point groups
  polyhedron.py         half-space intersection, face loops, areas, volume
  habit.py              forms -> crystal, relative-development solvers
  export.py             STL, STEP (AP214) and JSON writers
  minerals/             one module per mineral: lattice, forms, matrix definition, literature
  build.py              builds everything
models/stl/<mineral>/   one STL per matrix cell
models/step/<mineral>/  one STEP per matrix cell (faces are named by their Miller index)
site/                   static three.js site (deployed to GitHub Pages with models/)
  geom.js               browser half-space clipper (same construction as the generator)
  views.js              three.js rendering: grid of scissor viewports, orbit views, arrows
  app.js / learn.js     matrix + inspector, and the step-by-step Learn walkthrough
scripts/serve.py        local preview server
```

## Usage

```bash
pip install -r requirements.txt
python -m habitmatrix.build            # rebuild all models + site data
python -m habitmatrix.build zircon     # or a single mineral
python scripts/serve.py                # preview at http://127.0.0.1:8765
```

Custom habit in Python:

```python
from habitmatrix.minerals import zircon
from habitmatrix.minerals._common import prism_then_cap
from habitmatrix.export import write_step

zr = zircon.crystal()
d, t = prism_then_cap(zr, {"100": 1, "110": 1, "101": 1.2, "211": 1.2},
                      prism=("100", "110", 0.7),   # {100} is 70 % of the prism cross-section
                      cap=("101", "211", 0.3),     # {101} is 30 % of the pyramid area
                      aspect=3.0)
write_step(zr.solid(d, t), "my_zircon.step")
```

## Validation

```bash
freecadcmd -c "exec(open('scripts/validate_models.py').read())"   # run from the repo root
```

FreeCAD (OpenCASCADE) reads every STEP file as one valid, closed solid of unit volume, and every STL file
is a closed, manifold mesh of the same volume.

## Caveats

These are idealized convex, unabraded, untwinned, unzoned habits. Some relative-development scales (for
example Pupin's index increments) are qualitative in the source papers, and the mapping used here is
documented in each mineral module and on the website.
