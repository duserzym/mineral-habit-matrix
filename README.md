# Mineral Habit Matrix

**Live site:** https://duserzym.github.io/mineral-habit-matrix/

This repo generates grids ("habit matrices") of idealized 3D crystal geometries for 41 rock-forming,
accessory and ore minerals (720 crystals). Zircon follows the Pupin (1980) typology. The other
minerals use habit series taken from the morphology and grain-geometry literature that is cited on the site.
Every face index is given in the structural cell. Where classical morphology used a different cell (for example
calcite, staurolite, cordierite, vesuvianite, orthopyroxene, gypsum and barite), the conversion was checked
against Dana's (1892) interfacial angles. Minerals without robust habit data (for example wollastonite, chlorite,
lawsonite and pyrrhotite) were left out.

| Group | Mineral | Matrix | Cells | Chronometers / uses |
|---|---|---|---|---|
| Accessory chronometers | Zircon | Pupin (1980) typology grid | 64 | U–Pb, (U–Th)/He, fission track, Lu–Hf, Ti-in-zircon |
| Accessory chronometers | Xenotime | Dipyramid → prism | 12 | U–Th–Pb, diagenetic/hydrothermal dating, monazite–xenotime thermometry |
| Accessory chronometers | Apatite | Termination × elongation | 20 | (U–Th)/He, fission track, U–Pb, Sm–Nd |
| Accessory chronometers | Monazite | Tabular on {100} × elongation along b | 16 | U–Th–Pb (EPMA, LA-ICP-MS, SIMS), (U–Th)/He |
| Accessory chronometers | Titanite | Envelope → prismatic → tabular | 16 | U–Pb, (U–Th)/He, Zr-in-titanite thermometry |
| Accessory chronometers | Rutile | Prism × termination grid | 16 | U–Pb, Zr-in-rutile thermometry, (U–Th)/He |
| Framework silicates | Quartz | Prism length × rhombohedron balance | 25 | Ti-in-quartz thermometry; OSL/ESR dating; cosmogenic nuclides |
| Framework silicates | K-feldspar | Flattening on (010) × elongation axis | 25 | ⁴⁰Ar/³⁹Ar multi-diffusion-domain (MDD) thermochronology; Pb isotopes |
| Framework silicates | Plagioclase | (010) tabularity × elongation along [100] | 20 | Diffusion chronometry (Mg, Sr); crystal size distributions; ⁴⁰Ar/³⁹Ar |
| Framework silicates | Nepheline | Prism length × prism modification | 20 | Composition as a crystallization thermometer |
| Framework silicates | Leucite | Icositetrahedron with cube and dodecahedron | 16 | ⁴⁰Ar/³⁹Ar (K-rich volcanic rocks); crystal size distributions |
| Framework silicates | Sodalite | Dodecahedron with cube and tetrahedron | 16 | — |
| Orthosilicates | Olivine | Tabular ↔ elongate × form complexity | 20 | Fe–Mg, Ni, Ca diffusion chronometry (magma timescales) |
| Orthosilicates | Garnet | Dodecahedron ↔ trapezohedron | 15 | Sm–Nd, Lu–Hf, U–Pb, diffusion speedometry |
| Orthosilicates | Kyanite | Blade elongation × flattening on (100) | 16 | Al₂SiO₅ polymorph thermobarometry; inclusion barometry |
| Orthosilicates | Andalusite | Termination × elongation | 16 | Al₂SiO₅ polymorph thermobarometry (contact aureoles) |
| Orthosilicates | Sillimanite | Prism zone × elongation | 16 | Al₂SiO₅ polymorph thermobarometry |
| Orthosilicates | Staurolite | Prism section × elongation | 16 | Metapelite thermobarometry (index mineral) |
| Sorosilicates | Epidote | Prism zone × elongation along b | 16 | U–Pb (hydrothermal veins); Sr, Pb isotopes |
| Sorosilicates | Zoisite | Prism zone × elongation along b | 9 | Sr–Pb isotopes; HP metamorphism (eclogite) petrology |
| Sorosilicates | Vesuvianite | Prism length × termination | 15 | Skarn and rodingite petrology |
| Ring silicates | Tourmaline | Prism section × elongation (hemimorphic) | 16 | B-isotope and sector-zoning thermometry; provenance |
| Ring silicates | Cordierite | Pseudo-hexagonal prism × elongation | 16 | Channel H₂O/CO₂ as a fluid record; low-P metamorphic thermobarometry |
| Chain silicates | Orthopyroxene | Prism cross-section × elongation | 20 | Fe–Mg diffusion chronometry; two-pyroxene thermometry |
| Chain silicates | Clinopyroxene | Prism cross-section × elongation | 16 | Fe–Mg diffusion chronometry; sector-zoning records of ascent |
| Chain silicates | Amphibole | Prism cross-section × elongation | 16 | ⁴⁰Ar/³⁹Ar, K–Ar |
| Sheet silicates | Biotite | Plate outline × thickness | 16 | ⁴⁰Ar/³⁹Ar, K–Ar, Rb–Sr |
| Sheet silicates | Muscovite | Plate outline × thickness | 16 | ⁴⁰Ar/³⁹Ar, K–Ar, Rb–Sr |
| Carbonates | Calcite | Prism length × termination | 20 | U–Pb carbonate dating; clumped isotopes; δ¹⁸O, δ¹³C |
| Carbonates | Dolomite | Basal development × rhombohedron | 12 | U–Pb carbonate dating; clumped isotopes; diagenetic thermometry |
| Carbonates | Aragonite | Prism length × termination | 16 | U-series dating (corals, speleothems); δ¹⁸O, Sr/Ca, clumped isotopes |
| Sulfates | Gypsum | Elongation × termination | 16 | Sr, S and O isotopes of evaporites; fluid inclusions |
| Sulfates | Anhydrite | Elongation along a × tabularity on (010) | 9 | Sr and S isotopes (seawater–hydrothermal mixing) |
| Sulfates | Barite | (001) tabularity × tablet outline | 16 | Marine barite Sr and S isotopes; export-productivity proxy |
| Halides | Halite | Cube ↔ octahedron × dodecahedron | 15 | Fluid-inclusion paleothermometry; evaporite Br/Cl |
| Halides | Fluorite | Cube ↔ octahedron × modifier | 20 | Sm–Nd dating of mineralization; REE fluid tracer |
| Oxides | Magnetite | Octahedron ↔ dodecahedron | 15 | (U–Th)/He; remanence carrier in paleomagnetism |
| Oxides | Hematite | Rhombohedral → specular plates | 12 | (U–Th)/He, (U–Th)/Ne; remanence carrier in paleomagnetism |
| Oxides | Spinel / chromite | Octahedron with dodecahedron and cube | 12 | Cr# as a melting and tectonic-setting indicator |
| Oxides | Ilmenite | Tabularity × lateral forms | 16 | Fe–Ti two-oxide thermometry and oxybarometry; remanence (hemo-ilmenite) |
| Sulfides | Pyrite | Cube ↔ octahedron × pyritohedron | 20 | Re–Os dating; trace-element (Au, As) zoning; S isotopes |

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
scripts/make_icon.py    draws the zircon icon (site/icon.svg) from the generator's own geometry
scripts/check_dois.py   checks every reference DOI against Crossref
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
is a closed, manifold mesh of the same volume (720/720 pass).

## Caveats

These are idealized convex, unabraded, untwinned, unzoned habits. Some relative-development scales (for
example Pupin's index increments) are qualitative in the source papers, and the mapping used here is
documented in each mineral module and on the website.
