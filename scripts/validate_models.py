"""Validate every STEP and STL file with FreeCAD (OpenCASCADE).

    freecadcmd -c "exec(open('scripts/validate_models.py').read())"

Checks that each STEP is one valid, closed solid whose volume is 1 (unit-volume
normalization) and that each STL is a closed, manifold mesh with the same volume.
"""

import glob
import os

import Mesh  # noqa: F401  (FreeCAD modules)
import Part

root = os.environ.get("HABIT_ROOT", os.getcwd())
bad = []
n = 0
for step in sorted(glob.glob(os.path.join(root, "models", "step", "*", "*.step"))):
    n += 1
    s = Part.read(step)
    stl = step.replace(os.sep + "step" + os.sep, os.sep + "stl" + os.sep)[:-5] + ".stl"
    m = Mesh.Mesh(stl)
    ok = (s.isValid() and s.isClosed() and len(s.Solids) == 1 and abs(s.Volume - 1) < 1e-4
          and m.isSolid() and not m.hasNonManifolds() and abs(m.Volume - 1) < 1e-3)
    if not ok:
        bad.append((os.path.basename(step), s.isValid(), s.isClosed(), len(s.Solids), s.Volume, m.isSolid(), m.Volume))
print(f"checked {n} STEP/STL pairs; {len(bad)} problems")
for b in bad:
    print("  ", b)
