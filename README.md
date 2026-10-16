# Mineral Habit Matrix

**Live site:** https://duserzym.github.io/mineral-habit-matrix/

This repo generates grids ("habit matrices") of idealized 3D crystal geometries for petrochronometer and
thermochronometer minerals. Zircon follows the Pupin (1980) typology. The other minerals use habit
series taken from the morphology and grain-geometry literature that is cited on the site.

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
site/                   static three.js viewer (deployed to GitHub Pages with models/)
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

FreeCAD (`Part.read`) reads every STEP file as one valid, closed solid, and the volumes and
areas match the generator's own values. The STL files are closed 2-manifold meshes.

## Caveats

These are idealized convex, unabraded, untwinned, unzoned habits. Some relative-development scales (for
example Pupin's index increments) are qualitative in the source papers, and the mapping used here is
documented in each mineral module and on the website.
