import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { radius as solidRadius } from './geom.js';

const dark = () => document.documentElement.dataset.theme === 'dark'
  || (document.documentElement.dataset.theme !== 'light' && matchMedia('(prefers-color-scheme: dark)').matches);

export function makeRenderer(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  // phones: cap the pixel ratio to keep many viewports smooth and battery-friendly
  const coarse = matchMedia('(pointer: coarse)').matches;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, coarse ? 1.5 : 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.setClearColor(0x000000, 0);
  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  const key = new THREE.DirectionalLight(0xffffff, 1.4);
  key.position.set(2.5, 4, 5);
  const rim = new THREE.DirectionalLight(0xffe6cc, 0.5);
  rim.position.set(-4, 1, -3);
  scene.add(key, rim);
  return { renderer, scene };
}

// Default view in the spirit of clinographic crystal drawings: c-axis up, turned about it
// and tipped towards the viewer.
export const viewQ = (tilt = 12, turn = -24) => new THREE.Quaternion()
  .setFromEuler(new THREE.Euler(THREE.MathUtils.degToRad(tilt), THREE.MathUtils.degToRad(turn), 0, 'XYZ'));

/**
 * A crystal as a three.js group.  Crystal frame: c = +z; the inner group maps it to three's +y.
 * faces: [{form, n, loop: [[x,y,z]...]}]; form 'box' faces (unbounded directions) are drawn as glass.
 */
export function crystalObject(faces, data, { color = 'form', opacity = 1, edges = true, highlight = null } = {}) {
  const forms = Object.fromEntries(data.forms.map((f) => [f.key, f]));
  const pos = [], col = [], nrm = [], bpos = [], bnrm = [], epos = [];
  const c = new THREE.Color();
  const mono = new THREE.Color(data.mono_color || '#c9a27a');
  const seen = new Set();
  for (const f of faces) {
    const box = f.form === 'box';
    const [P, N] = box ? [bpos, bnrm] : [pos, nrm];
    if (!box) {
      c.set(color === 'mono' ? mono : forms[f.form]?.color || '#999');
      if (highlight && f.form !== highlight) c.lerp(new THREE.Color(dark() ? '#333' : '#ddd'), 0.65);
    }
    const L = f.loop;
    for (let j = 1; j < L.length - 1; j++) {
      for (const q of [L[0], L[j], L[j + 1]]) {
        P.push(...q); N.push(...f.n);
        if (!box) col.push(c.r, c.g, c.b);
      }
    }
    for (let j = 0; j < L.length; j++) {
      const a = L[j], b = L[(j + 1) % L.length];
      const k = [a, b].map((p) => p.map((x) => x.toFixed(5)).join(',')).sort().join('|');
      if (seen.has(k)) continue;
      seen.add(k);
      epos.push(...a, ...b);
    }
  }
  const crystal = new THREE.Group();
  crystal.rotation.x = -Math.PI / 2;
  if (pos.length) {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    g.setAttribute('normal', new THREE.Float32BufferAttribute(nrm, 3));
    g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    const mat = new THREE.MeshPhysicalMaterial({
      vertexColors: true, roughness: 0.3, metalness: 0, clearcoat: 0.85, clearcoatRoughness: 0.1,
      transparent: opacity < 1, opacity, depthWrite: opacity >= 1,
      polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1, side: opacity < 1 ? THREE.DoubleSide : THREE.FrontSide,
    });
    crystal.add(new THREE.Mesh(g, mat));
  }
  if (bpos.length) {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(bpos, 3));
    g.setAttribute('normal', new THREE.Float32BufferAttribute(bnrm, 3));
    crystal.add(new THREE.Mesh(g, new THREE.MeshPhysicalMaterial({
      color: dark() ? 0x8aa0c0 : 0x9fb6d8, transparent: true, opacity: 0.18, roughness: 0.1,
      depthWrite: false, side: THREE.DoubleSide,
    })));
  }
  const eg = new THREE.BufferGeometry();
  eg.setAttribute('position', new THREE.Float32BufferAttribute(epos, 3));
  const lines = new THREE.LineSegments(eg, new THREE.LineBasicMaterial({
    color: dark() ? 0x0b0a08 : 0x2a2018, transparent: true, opacity: 0.55,
  }));
  lines.visible = edges;
  crystal.add(lines);
  const holder = new THREE.Group();
  holder.add(crystal);
  holder.userData = { radius: solidRadius(faces.filter((f) => f.form !== 'box').length ? faces.filter((f) => f.form !== 'box') : faces), edges: lines, inner: crystal };
  return holder;
}

export function dispose(obj) {
  obj?.traverse((o) => {
    o.geometry?.dispose();
    if (o.material) (Array.isArray(o.material) ? o.material : [o.material]).forEach((m) => { m.map?.dispose(); m.dispose(); });
  });
  obj?.parent?.remove(obj);
}

/** Text label that always faces the camera. */
export function label(text, color = '#222', size = 0.12) {
  const cv = document.createElement('canvas');
  const ctx = cv.getContext('2d');
  const font = '600 44px -apple-system, BlinkMacSystemFont, "SF Pro Text", Inter, sans-serif';
  ctx.font = font;
  const w = Math.ceil(ctx.measureText(text).width) + 24;
  cv.width = w; cv.height = 64;
  ctx.font = font;
  ctx.fillStyle = color;
  ctx.textBaseline = 'middle';
  ctx.fillText(text, 12, 34);
  const tex = new THREE.CanvasTexture(cv);
  tex.colorSpace = THREE.SRGBColorSpace;
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: false, transparent: true }));
  sp.scale.set((size * w) / 64, size, 1);
  sp.renderOrder = 10;
  return sp;
}

/** Arrow (crystal frame) from origin along v with a label at its tip. */
export function vectorArrow(v, color, text, r, { from = [0, 0, 0], head = 0.12 } = {}) {
  const g = new THREE.Group();
  const dir = new THREE.Vector3(...v);
  const L = dir.length();
  const a = new THREE.ArrowHelper(dir.clone().normalize(), new THREE.Vector3(...from), L, color, head * r, head * r * 0.55);
  a.line.material.linewidth = 2;
  g.add(a);
  if (text) {
    const s = label(text, typeof color === 'string' ? color : `#${new THREE.Color(color).getHexString()}`, 0.16 * r);
    s.position.copy(new THREE.Vector3(...from).add(dir.clone().multiplyScalar(1.12)));
    g.add(s);
  }
  return g;
}

/** Unit-cell parallelepiped and a, b, c axes, scaled so the longest edge is k·r. */
export function cellFrame(basis, r, k = 1.1) {
  const g = new THREE.Group();
  const m = Math.max(...basis.map((v) => Math.hypot(...v)));
  const B = basis.map((v) => v.map((x) => (x * k * r) / m));
  const o = B[0].map((_, i) => -(B[0][i] + B[1][i] + B[2][i]) / 2);
  const P = (i, j, l) => o.map((x, q) => x + i * B[0][q] + j * B[1][q] + l * B[2][q]);
  const e = [];
  for (const [i, j, l] of [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]]) {
    if (!i) e.push(...P(i, j, l), ...P(1, j, l));
    if (!j) e.push(...P(i, j, l), ...P(i, 1, l));
    if (!l) e.push(...P(i, j, l), ...P(i, j, 1));
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(e, 3));
  g.add(new THREE.LineSegments(geo, new THREE.LineDashedMaterial({ color: dark() ? 0xdddddd : 0x333333, dashSize: 0.05 * r, gapSize: 0.04 * r, transparent: true, opacity: 0.7 })));
  g.children[0].computeLineDistances();
  const cols = ['#e5484d', '#30a46c', '#0090ff'];
  ['a', 'b', 'c'].forEach((n, i) => g.add(vectorArrow(B[i], cols[i], n, r, { from: o, head: 0.09 })));
  return g;
}

/** A single orbitable view rendered into its own canvas inside `container`. */
export class SoloView {
  constructor(container) {
    this.el = container;
    this.canvas = document.createElement('canvas');
    this.canvas.className = 'solo-gl';
    container.appendChild(this.canvas);
    Object.assign(this, makeRenderer(this.canvas));
    this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, -50, 50);
    this.camera.position.set(0, 0, 10);
    this.controls = new OrbitControls(this.camera, this.canvas);
    this.controls.enableDamping = true;
    this.controls.enablePan = false;
    this.controls.minZoom = 0.4;
    this.controls.maxZoom = 5;
    this.root = new THREE.Group();
    this.scene.add(this.root);
    this.radius = 1;
    this.fit = 1.2;
  }

  set(objects, radius, q = null) {
    for (const c of [...this.root.children]) dispose(c);
    for (const o of [].concat(objects)) if (o) this.root.add(o);
    if (radius) this.radius = radius;
    if (q) this.root.quaternion.copy(q);
  }

  resetView(q) {
    this.camera.position.set(0, 0, 10);
    this.camera.zoom = 1;
    this.controls.target.set(0, 0, 0);
    this.camera.updateProjectionMatrix();
    if (q) this.root.quaternion.copy(q);
  }

  frame() {
    const w = this.el.clientWidth, h = this.el.clientHeight;
    if (!w || !h) return;
    const pr = this.renderer.getPixelRatio();
    if (this.canvas.width !== Math.floor(w * pr) || this.canvas.height !== Math.floor(h * pr)) this.renderer.setSize(w, h, false);
    const s = this.radius * this.fit, a = w / h;
    const hx = a >= 1 ? s * a : s, hy = a >= 1 ? s : s / a; // fit the shorter side
    Object.assign(this.camera, { left: -hx, right: hx, top: hy, bottom: -hy });
    this.camera.updateProjectionMatrix();
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
}

/** Many crystals drawn with scissor viewports into one canvas laid over a grid of cells. */
export class GridView {
  constructor(stage, scroller) {
    this.stage = stage;
    this.scroller = scroller;
    this.canvas = document.createElement('canvas');
    this.canvas.className = 'grid-gl';
    stage.appendChild(this.canvas);
    Object.assign(this, makeRenderer(this.canvas));
    this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, -50, 50);
    this.items = []; // {el, obj}
    this.q = new THREE.Quaternion();
    this.scaleMode = 'fit';
  }

  setItems(items) {
    for (const it of this.items) dispose(it.obj);
    this.items = items;
    for (const it of items) { it.obj.visible = false; this.scene.add(it.obj); }
    this.maxR = Math.max(...items.map((i) => i.obj.userData.radius), 1e-6);
  }

  frame() {
    const S = this.stage.getBoundingClientRect();
    const pr = this.renderer.getPixelRatio();
    const W = Math.round(S.width), H = Math.round(S.height);
    if (!W || !H) return;
    if (this.canvas.width !== Math.floor(W * pr) || this.canvas.height !== Math.floor(H * pr)) this.renderer.setSize(W, H, false);
    const R = this.renderer;
    R.setScissorTest(false);
    R.clear();
    R.setScissorTest(true);
    const sc = this.scroller.getBoundingClientRect();
    const clip = {
      left: Math.max(sc.left, 0) - S.left, right: Math.min(sc.right, innerWidth) - S.left,
      top: Math.max(sc.top, 0) - S.top, bottom: Math.min(sc.bottom, innerHeight) - S.top,
    };
    // keep crystals from drawing over a sticky header column
    const sticky = this.stickyLeft?.();
    if (sticky) clip.left = Math.max(clip.left, sticky - S.left);
    for (const it of this.items) {
      const r = it.el.getBoundingClientRect();
      const box = { left: r.left - S.left, right: r.right - S.left, top: r.top - S.top, bottom: r.bottom - S.top };
      const vis = {
        left: Math.max(box.left, clip.left), right: Math.min(box.right, clip.right),
        top: Math.max(box.top, clip.top), bottom: Math.min(box.bottom, clip.bottom),
      };
      if (vis.right <= vis.left || vis.bottom <= vis.top) continue;
      const w = box.right - box.left, h = box.bottom - box.top;
      R.setViewport(box.left, H - box.bottom, w, h);
      R.setScissor(vis.left, H - vis.bottom, vis.right - vis.left, vis.bottom - vis.top);
      const s = (this.scaleMode === 'fit' ? it.obj.userData.radius : this.maxR) * 1.04;
      const a = w / h;
      Object.assign(this.camera, { left: -s * a, right: s * a, top: s, bottom: -s });
      this.camera.updateProjectionMatrix();
      if (!it.q) it.obj.quaternion.copy(this.q); // items with their own orientation keep it
      it.obj.visible = true;
      R.render(this.scene, this.camera);
      it.obj.visible = false;
    }
  }
}

/** Wrap helper objects (arrows, cell frame) in the crystal frame (c = +z -> three's +y). */
export function inCrystalFrame(...objs) {
  const g = new THREE.Group();
  const inner = new THREE.Group();
  inner.rotation.x = -Math.PI / 2;
  for (const o of objs) if (o) inner.add(o);
  g.add(inner);
  return g;
}

/** Translucent discs for face planes n·x = d (crystal frame): [{n, d, color}] with disc radius r. */
export function planeDiscs(planes, r, { opacity = 0.2 } = {}) {
  const g = new THREE.Group();
  if (planes.length > 6) { r *= Math.sqrt(6 / planes.length); opacity *= 0.8; } // keep many-faced forms readable
  const disc = new THREE.CircleGeometry(r, 48);
  const ring = new THREE.BufferGeometry().setFromPoints(
    Array.from({ length: 65 }, (_, i) => new THREE.Vector3(r * Math.cos((i / 32) * Math.PI), r * Math.sin((i / 32) * Math.PI), 0)));
  const Zv = new THREE.Vector3(0, 0, 1);
  for (const p of planes) {
    const n = new THREE.Vector3(...p.n).normalize();
    const holder = new THREE.Group();
    holder.quaternion.setFromUnitVectors(Zv, n);
    holder.position.copy(n.clone().multiplyScalar(p.d));
    const fill = new THREE.Mesh(disc, new THREE.MeshBasicMaterial({
      color: p.color, transparent: true, opacity, depthWrite: false, side: THREE.DoubleSide,
    }));
    const edge = new THREE.Line(ring, new THREE.LineBasicMaterial({ color: p.color, transparent: true, opacity: Math.min(1, opacity * 3.2) }));
    fill.userData.baseOpacity = opacity;
    edge.userData.baseOpacity = Math.min(1, opacity * 3.2);
    fill.renderOrder = edge.renderOrder = 5;
    holder.add(fill, edge);
    g.add(holder);
  }
  return inCrystalFrame(g);
}

/** Scale the opacity of every material under obj relative to its base opacity. */
export function fade(obj, k) {
  obj?.traverse((o) => {
    if (o.material && o.userData.baseOpacity != null) o.material.opacity = o.userData.baseOpacity * k;
  });
}

/** A symmetry element (from geom.describeOp) drawn at the crystal centre: axis, mirror plane or inversion centre. */
export function symmetryElement(op, r) {
  const col = dark() ? '#f5f5f7' : '#1d1d1f';
  const g = new THREE.Group();
  if (op.kind === 'rotation' || op.kind === 'rotoinversion') {
    const a = new THREE.Vector3(...op.axis).normalize();
    const geo = new THREE.BufferGeometry().setFromPoints([a.clone().multiplyScalar(-1.3 * r), a.clone().multiplyScalar(1.3 * r)]);
    const line = new THREE.Line(geo, new THREE.LineDashedMaterial({ color: col, dashSize: 0.08 * r, gapSize: 0.05 * r, transparent: true, opacity: 0.85, depthTest: false }));
    line.computeLineDistances();
    line.renderOrder = 8;
    g.add(line);
    for (const s of [1, -1]) {
      const sp = label(op.symbol, col, 0.2 * r);
      sp.position.copy(a.clone().multiplyScalar(s * 1.42 * r));
      g.add(sp);
    }
  } else if (op.kind === 'mirror') {
    const n = op.normal;
    const disc = planeDiscs([{ n, d: 0, color: dark() ? '#9fb6d8' : '#5b7db1' }], 1.35 * r, { opacity: 0.16 });
    g.add(disc.children[0].children[0]);
    const sp = label('m', col, 0.2 * r);
    const t = new THREE.Vector3(...n).cross(Math.abs(n[2]) < 0.9 ? new THREE.Vector3(0, 0, 1) : new THREE.Vector3(1, 0, 0)).normalize();
    sp.position.copy(t.multiplyScalar(1.45 * r));
    g.add(sp);
  } else {
    const dot_ = new THREE.Mesh(new THREE.SphereGeometry(0.05 * r, 20, 12), new THREE.MeshBasicMaterial({ color: col, depthTest: false }));
    dot_.renderOrder = 9;
    g.add(dot_);
    const sp = label('1̄  centre', col, 0.17 * r);
    sp.position.set(0.32 * r, 0, 0.12 * r);
    g.add(sp);
  }
  return inCrystalFrame(g);
}
