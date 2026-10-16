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
