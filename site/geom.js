// Crystal geometry in the browser: the same construction as the Python generator
// (reciprocal-lattice face normals -> symmetry-equivalent faces -> half-space intersection),
// implemented as successive clipping of a large cube by the planes  n·x <= d.

export const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
export const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
export const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
export const mul = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
export const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
export const len = (a) => Math.hypot(a[0], a[1], a[2]);
export const unit = (a) => mul(a, 1 / len(a));
export const deg = (r) => (r * 180) / Math.PI;
export const angle = (a, b) => deg(Math.acos(Math.max(-1, Math.min(1, dot(unit(a), unit(b))))));

/** Overbar notation, e.g. [1,0,-1,1] -> "101̄1" */
export const fmtIndex = (idx) => idx.map((x) => (x < 0 ? `${-x}̅` : `${x}`)).join('');

/** Effective central distance per form: s·(d + |n·u|·t)  (u = elongation axis). */
export function effectiveDistances(data, distances, t = 0, s = 1) {
  const out = {};
  for (const f of data.forms) {
    const d = distances[f.key];
    if (d == null) continue;
    const shift = data.axis ? Math.abs(dot(f.normals[0], data.axis)) : 0;
    out[f.key] = s * (d + shift * t);
  }
  return out;
}

/** Every face plane of the forms present: {form, hkl, n, d}. */
export function planesFor(data, dEff, onlyKeys = null) {
  const planes = [];
  for (const f of data.forms) {
    if (dEff[f.key] == null) continue;
    if (onlyKeys && !onlyKeys.includes(f.key)) continue;
    f.normals.forEach((n, i) => planes.push({ form: f.key, hkl: f.hkls[i], n, d: dEff[f.key] }));
  }
  return planes;
}

function cube(B) {
  const X = [1, 0, 0], Y = [0, 1, 0], Z = [0, 0, 1];
  const sides = [[X, Y, Z], [mul(X, -1), Z, Y], [Y, Z, X], [mul(Y, -1), X, Z], [Z, X, Y], [mul(Z, -1), Y, X]];
  return sides.map(([n, u, w]) => {
    const c = mul(n, B);
    const loop = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([a, b]) => add(c, add(mul(u, a * B), mul(w, b * B))));
    return { form: 'box', hkl: null, n, d: B, loop };
  });
}

function dedupe(pts, tol) {
  const out = [];
  for (const p of pts) if (!out.some((q) => len(sub(p, q)) < tol)) out.push(p);
  return out;
}

function orderLoop(pts, n) {
  const c = mul(pts.reduce((s, p) => add(s, p), [0, 0, 0]), 1 / pts.length);
  let u = sub(pts[0], c);
  u = unit(sub(u, mul(n, dot(u, n))));
  const w = cross(n, u);
  return pts
    .map((p) => [Math.atan2(dot(sub(p, c), w), dot(sub(p, c), u)), p])
    .sort((a, b) => a[0] - b[0])
    .map((x) => x[1]);
}

/** Clip a convex solid (list of faces) by one half-space. */
export function clipBy(faces, { n, d, form, hkl }, scale) {
  const eps = 1e-9 * scale, tol = 1e-7 * scale;
  const out = [];
  const cap = [];
  for (const f of faces) {
    const P = f.loop;
    const res = [];
    for (let i = 0; i < P.length; i++) {
      const cur = P[i], prev = P[(i + P.length - 1) % P.length];
      const dc = dot(n, cur) - d, dp = dot(n, prev) - d;
      const cut = () => { const x = add(prev, mul(sub(cur, prev), dp / (dp - dc))); res.push(x); cap.push(x); };
      if (dc <= eps) {
        if (dp > eps) cut();
        res.push(cur);
        if (Math.abs(dc) <= eps) cap.push(cur);
      } else if (dp < -eps) {
        cut();
      }
    }
    const loop = dedupe(res, tol);
    if (loop.length >= 3 && faceArea({ n: f.n, loop }) > tol * tol) out.push({ ...f, loop });
  }
  const pts = dedupe(cap, tol);
  if (pts.length >= 3) {
    const face = { form, hkl, n, d, loop: orderLoop(pts, n) };
    if (faceArea(face) > tol * tol) out.push(face);
  }
  return out;
}

/** Intersect half-spaces, starting from a cube of half-size B (faces of the cube that
 *  survive are flagged form = 'box': they mark directions in which the solid is unbounded). */
export function solidFrom(planes, B = null) {
  const R = B ?? 6 * Math.max(...planes.map((p) => p.d), 1e-3);
  let faces = cube(R);
  for (const p of planes) faces = clipBy(faces, p, R);
  return faces;
}

export function faceArea(f) {
  const P = f.loop;
  let s = [0, 0, 0];
  for (let i = 1; i < P.length - 1; i++) s = add(s, cross(sub(P[i], P[0]), sub(P[i + 1], P[0])));
  return 0.5 * Math.abs(dot(s, f.n));
}

export function formAreas(faces) {
  const a = {};
  for (const f of faces) if (f.form !== 'box') a[f.form] = (a[f.form] || 0) + faceArea(f);
  return a;
}

export function volume(faces) {
  return faces.reduce((v, f) => v + (faceArea(f) * dot(f.n, f.loop[0])) / 3, 0);
}

export function radius(faces) {
  let r = 0;
  for (const f of faces) for (const p of f.loop) r = Math.max(r, len(p));
  return r;
}

/** Faces from the precomputed JSON geometry of a matrix cell. */
export function facesFromJSON(geometry, data) {
  const V = geometry.vertices;
  return geometry.faces.map((f) => {
    const loop = f.loop.map((i) => V[i]);
    const n = unit(cross(sub(loop[1], loop[0]), sub(loop[2], loop[0])));
    return { form: f.form, hkl: f.hkl, n, loop };
  });
}

/** Length of the solid along u divided by its largest width normal to u. */
export function aspect(faces, u) {
  const pts = faces.flatMap((f) => f.loop);
  const ext = (v) => { const p = pts.map((x) => dot(x, v)); return Math.max(...p) - Math.min(...p); };
  if (!u) return 1;
  let e1 = cross(u, Math.abs(u[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0]);
  e1 = unit(e1);
  const e2 = cross(u, e1);
  let w = 0;
  for (let k = 0; k < 36; k++) {
    const a = (Math.PI * k) / 36;
    w = Math.max(w, ext(add(mul(e1, Math.cos(a)), mul(e2, Math.sin(a)))));
  }
  return ext(u) / w;
}

// ---------------------------------------------------------------------------
// Point-group symmetry, ported from habitmatrix/lattice.py (same Cartesian frame:
// c along z, b in the yz-plane). Matrices are arrays of rows.

const I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
export const apply = (M, v) => [dot(M[0], v), dot(M[1], v), dot(M[2], v)];
export const matmul = (A, B) => A.map((r) => [0, 1, 2].map((j) => r[0] * B[0][j] + r[1] * B[1][j] + r[2] * B[2][j]));
const det = (M) => dot(M[0], cross(M[1], M[2]));
const neg = (M) => M.map((r) => r.map((x) => -x));
const same = (A, B) => A.every((r, i) => r.every((x, j) => Math.abs(x - B[i][j]) < 1e-9));

/** Rotation about `axis` by `deg` degrees (Rodrigues). */
export function rotation(axis, deg) {
  const [x, y, z] = unit(axis), t = (deg * Math.PI) / 180, c = Math.cos(t), s = Math.sin(t), C = 1 - c;
  return [
    [c + x * x * C, x * y * C - z * s, x * z * C + y * s],
    [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
    [z * x * C - y * s, z * y * C + x * s, c + z * z * C],
  ];
}

const mirror = (n) => { const u = unit(n); return I3.map((r, i) => r.map((x, j) => x - 2 * u[i] * u[j])); };
const INV = neg(I3);
const X = [1, 0, 0], Y = [0, 1, 0], Z = [0, 0, 1], D111 = [1, 1, 1], A1 = [Math.sqrt(3) / 2, -0.5, 0];
const GENERATORS = {
  '1': [], '-1': [INV], '2': [rotation(Y, 180)], 'm': [mirror(Y)], '2/m': [rotation(Y, 180), INV],
  '222': [rotation(Z, 180), rotation(Y, 180)], 'mm2': [rotation(Z, 180), mirror(X)], 'mmm': [rotation(Z, 180), rotation(Y, 180), INV],
  '4': [rotation(Z, 90)], '-4': [matmul(INV, rotation(Z, 90))], '4/m': [rotation(Z, 90), INV],
  '422': [rotation(Z, 90), rotation(X, 180)], '4mm': [rotation(Z, 90), mirror(X)], '-42m': [matmul(INV, rotation(Z, 90)), rotation(X, 180)],
  '4/mmm': [rotation(Z, 90), mirror(X), INV],
  '3': [rotation(Z, 120)], '-3': [rotation(Z, 120), INV], '32': [rotation(Z, 120), rotation(A1, 180)],
  '3m': [rotation(Z, 120), mirror(A1)], '-3m': [rotation(Z, 120), mirror(A1), INV],
  '6': [rotation(Z, 60)], '-6': [matmul(INV, rotation(Z, 60))], '6/m': [rotation(Z, 60), INV],
  '622': [rotation(Z, 60), rotation(A1, 180)], '6mm': [rotation(Z, 60), mirror(A1)], '-6m2': [matmul(INV, rotation(Z, 60)), mirror(A1)],
  '6/mmm': [rotation(Z, 60), mirror(A1), INV],
  '23': [rotation(Z, 180), rotation(D111, 120)], 'm-3': [rotation(Z, 180), rotation(D111, 120), INV],
  '432': [rotation(Z, 90), rotation(D111, 120)], '-43m': [matmul(INV, rotation(Z, 90)), rotation(D111, 120)],
  'm-3m': [rotation(Z, 90), rotation(D111, 120), INV],
};

export const generators = (symbol) => GENERATORS[symbol] || [];

/** Axis and angle (0..180°) of a proper rotation. */
function axisAngle(M) {
  const ang = deg(Math.acos(Math.max(-1, Math.min(1, (M[0][0] + M[1][1] + M[2][2] - 1) / 2))));
  if (ang < 1e-6) return { axis: Z, angle: 0 };
  let a = [M[2][1] - M[1][2], M[0][2] - M[2][0], M[1][0] - M[0][1]];
  if (len(a) < 1e-6) { // 180°: M + I = 2 a aᵀ
    const P = [0, 1, 2].map((j) => [M[0][j] + (j === 0), M[1][j] + (j === 1), M[2][j] + (j === 2)]);
    a = P.reduce((b, c) => (len(c) > len(b) ? c : b));
  }
  return { axis: unit(a), angle: ang };
}

/** What kind of symmetry element an operation is: rotation n, mirror m, inversion 1̄ or rotoinversion n̄. */
export function describeOp(M) {
  if (det(M) > 0) {
    const { axis, angle: a } = axisAngle(M);
    return { kind: 'rotation', axis, angle: a, order: Math.round(360 / a), symbol: `${Math.round(360 / a)}` };
  }
  const P = neg(M);
  if (same(P, I3)) return { kind: 'inversion', symbol: '1̄', order: 2 };
  const { axis, angle: a } = axisAngle(P);
  if (Math.abs(a - 180) < 1e-6) return { kind: 'mirror', normal: axis, symbol: 'm', order: 2 };
  const n = Math.round(360 / a);
  return { kind: 'rotoinversion', axis, symbol: `${n}̄`, order: n % 2 ? 2 * n : n };
}

/** The operation M applied a fraction s of the way: proper rotations turn, improper ones slide through the element. */
export function partialOp(M, s) {
  if (det(M) > 0) {
    const { axis, angle: a } = axisAngle(M);
    // keep the turn direction of M (axisAngle may return either sign of the axis for 180°)
    const R = rotation(axis, a);
    return same(R, M) || a > 179.999 ? rotation(axis, a * s) : rotation(axis, -a * s);
  }
  return I3.map((r, i) => r.map((x, j) => (1 - s) * x + s * M[i][j]));
}

/**
 * How symmetry builds each form from one face, as a list of stages. Each stage applies one generator
 * (with all its powers) to the faces made so far: {op, moves: [{form, from, to, M}]}.
 */
export function symmetryStages(forms, symbol) {
  const gens = generators(symbol);
  const has = (set, v) => set.some((w) => len(sub(v, w)) < 1e-6);
  const sets = Object.fromEntries(forms.map((f) => [f.key, [f.normals[0]]]));
  const stages = [];
  for (let pass = 0, grew = true; grew && pass < 6; pass++) {
    grew = false;
    for (const g of gens) {
      const info = describeOp(g);
      const powers = [g];
      while (powers.length < 12 && !same(powers[powers.length - 1], I3)) powers.push(matmul(g, powers[powers.length - 1]));
      powers.pop(); // the identity
      const moves = [];
      for (const f of forms) {
        const set = sets[f.key], add_ = [];
        for (const x of set) powers.forEach((M, i) => {
          const y = apply(M, x);
          if (!has(set, y) && !has(add_, y)) { add_.push(y); moves.push({ form: f.key, from: x, to: y, M, k: i + 1 }); }
        });
        set.push(...add_);
      }
      if (moves.length) { stages.push({ op: info, g, moves, counts: Object.fromEntries(forms.map((f) => [f.key, sets[f.key].length])) }); grew = true; }
    }
  }
  return stages;
}
