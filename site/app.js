import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

// ---------------------------------------------------------------- renderer
const canvas = $('#gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.setClearColor(0x000000, 0);

const scene = new THREE.Scene();
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
const keyLight = new THREE.DirectionalLight(0xffffff, 1.4);
keyLight.position.set(2.5, 4, 5);
scene.add(keyLight);
const rim = new THREE.DirectionalLight(0xffe6cc, 0.5);
rim.position.set(-4, 1, -3);
scene.add(rim);

const gridCam = new THREE.OrthographicCamera(-1, 1, 1, -1, -50, 50);
const detailCam = new THREE.OrthographicCamera(-1, 1, 1, -1, -50, 50);
detailCam.position.set(0, 0, 10);
const detailEl = $('#detail-view');
const controls = new OrbitControls(detailCam, detailEl);
controls.enableDamping = true;
controls.enablePan = false;
controls.minZoom = 0.5;
controls.maxZoom = 4;

// Default view in the spirit of clinographic crystal drawings: c-axis up, turned about it
// and tipped towards the viewer.  Plates (mica) use a steeper tilt, set per mineral.
const viewQ = (tilt = 12, turn = -24) => new THREE.Quaternion()
  .setFromEuler(new THREE.Euler(THREE.MathUtils.degToRad(tilt), THREE.MathUtils.degToRad(turn), 0, 'XYZ'));
let DEFAULT_Q = viewQ();
const gridQ = DEFAULT_Q.clone();
let spinAngle = 0;

const state = {
  index: [], data: null, cells: [], selected: null, detail: null,
  spin: true, edges: true, scale: 'fit', color: 'form', radius: 1,
};

// --------------------------------------------------------------- geometry
function buildCrystal(cell, data, colorMode) {
  const V = cell.geometry.vertices;
  const forms = Object.fromEntries(data.forms.map((f) => [f.key, f]));
  const pos = [];
  const col = [];
  const nrm = [];
  const edgePos = [];
  const seen = new Set();
  const c = new THREE.Color();
  const mono = new THREE.Color(data.mono_color || '#c9a27a');
  for (const f of cell.geometry.faces) {
    const loop = f.loop;
    const p = loop.map((i) => new THREE.Vector3(...V[i]));
    const n = new THREE.Vector3().crossVectors(p[1].clone().sub(p[0]), p[2].clone().sub(p[0])).normalize();
    c.set(colorMode === 'mono' ? mono : forms[f.form]?.color || '#999');
    for (let j = 1; j < p.length - 1; j++) {
      for (const q of [p[0], p[j], p[j + 1]]) { pos.push(q.x, q.y, q.z); col.push(c.r, c.g, c.b); nrm.push(n.x, n.y, n.z); }
    }
    for (let j = 0; j < loop.length; j++) {
      const a = loop[j], b = loop[(j + 1) % loop.length];
      const k = a < b ? `${a}-${b}` : `${b}-${a}`;
      if (seen.has(k)) continue;
      seen.add(k);
      edgePos.push(...V[a], ...V[b]);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('normal', new THREE.Float32BufferAttribute(nrm, 3));
  g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
  const mat = new THREE.MeshPhysicalMaterial({
    vertexColors: true, roughness: 0.32, metalness: 0.0, clearcoat: 0.8, clearcoatRoughness: 0.12,
    specularIntensity: 0.6, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1,
  });
  const mesh = new THREE.Mesh(g, mat);
  const eg = new THREE.BufferGeometry();
  eg.setAttribute('position', new THREE.Float32BufferAttribute(edgePos, 3));
  const edges = new THREE.LineSegments(eg, new THREE.LineBasicMaterial({ color: 0x2a2018, transparent: true, opacity: 0.55 }));
  edges.visible = state.edges;
  // crystal frame: c-axis = +z  ->  three.js +y (up)
  const crystal = new THREE.Group();
  crystal.rotation.x = -Math.PI / 2;
  crystal.add(mesh, edges);
  const holder = new THREE.Group();
  holder.add(crystal);
  holder.visible = false;
  let r = 0;
  for (const v of V) r = Math.max(r, Math.hypot(...v));
  holder.userData = { radius: r, mesh, edges };
  return holder;
}

function disposeGroup(g) {
  g.traverse((o) => { o.geometry?.dispose(); o.material?.dispose(); });
  scene.remove(g);
}

// ---------------------------------------------------------------- UI
async function init() {
  state.index = await (await fetch('data/index.json', { cache: 'no-cache' })).json();
  const tabs = $('#tabs');
  tabs.setAttribute('role', 'tablist');
  for (const m of state.index) {
    const b = document.createElement('button');
    b.className = 'tab';
    b.type = 'button';
    b.setAttribute('role', 'tab');
    b.dataset.id = m.id;
    b.innerHTML = `${esc(m.name)}<small>${m.ncells}</small>`;
    b.onclick = () => loadMineral(m.id, true);
    tabs.appendChild(b);
  }
  const fromHash = location.hash.slice(1).split('/')[0];
  const first = state.index.find((m) => m.id === fromHash) ? fromHash : state.index[0].id;
  await loadMineral(first, false);

  $('#opt-rotate').onchange = (e) => { state.spin = e.target.checked; };
  $('#opt-edges').onchange = (e) => {
    state.edges = e.target.checked;
    for (const c of state.cells) c.obj.userData.edges.visible = state.edges;
    if (state.detail) state.detail.userData.edges.visible = state.edges;
  };
  $('#opt-scale').onchange = (e) => { state.scale = e.target.value; };
  $('#opt-color').onchange = (e) => { state.color = e.target.value; rebuildObjects(); };
  $('#opt-reset').onclick = () => { gridQ.copy(DEFAULT_Q); spinAngle = 0; controls.reset(); };
  window.addEventListener('hashchange', () => {
    const id = location.hash.slice(1).split('/')[0];
    if (id && id !== state.data?.id && state.index.find((m) => m.id === id)) loadMineral(id, false);
  });
  setupDrag();
  requestAnimationFrame(loop);
}

async function loadMineral(id, push) {
  const entry = state.index.find((m) => m.id === id);
  const data = await (await fetch(`data/${entry.file}`, { cache: 'no-cache' })).json();
  state.data = data;
  DEFAULT_Q = viewQ(data.view?.tilt, data.view?.turn);
  gridQ.copy(DEFAULT_Q);
  for (const b of document.querySelectorAll('.tab')) b.setAttribute('aria-selected', String(b.dataset.id === id));
  if (push) history.replaceState(null, '', `#${id}`);

  $('#m-title').textContent = data.matrix.title;
  $('#m-sub').innerHTML = data.matrix.subtitle || '';
  $('#m-note').innerHTML = data.matrix.note || '';

  // legend + lattice
  $('#legend').innerHTML = data.forms.map((f) =>
    `<li><span class="sw" style="background:${f.color}"></span><code>${esc(f.label)}</code><span class="muted">${esc(f.name)}</span></li>`).join('');
  const L = data.lattice;
  const latRows = [
    ['System', `${data.system} · ${data.point_group}`],
    ['Setting', data.setting],
    ['a, b, c (Å)', `${L.a}, ${L.b}, ${L.c}`],
    ['α, β, γ', `${L.alpha}°, ${L.beta}°, ${L.gamma}°`],
    ['Cell source', data.lattice_source],
    ['Chronometers', data.chronometers],
  ];
  $('#lattice').innerHTML = latRows.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('');

  // about
  const habits = (data.habits || []).map((h) => `<li><strong>${esc(h.name)}.</strong> ${h.text}</li>`).join('');
  $('#about-mineral').innerHTML = `<h2>${esc(data.name)}: habits &amp; morphology</h2>${data.about || ''}${habits ? `<ul class="habits">${habits}</ul>` : ''}`;

  // references
  $('#refs').innerHTML = (data.references || []).map((r) => {
    const link = r.doi ? `<a href="https://doi.org/${esc(r.doi)}" target="_blank" rel="noopener">doi:${esc(r.doi)}</a>`
      : r.url ? `<a href="${esc(r.url)}" target="_blank" rel="noopener">link</a>` : '';
    const tags = (r.tags || []).map((t) => `<span class="tag">${esc(t)}</span>`).join('');
    return `<li>${r.citation} ${link}${tags}<span class="why">${r.note || ''}</span></li>`;
  }).join('');

  buildMatrix(data);
  const sel = location.hash.split('/')[1];
  selectCell(state.cells.find((c) => c.data.id === sel) || state.cells.find((c) => c.data.default) || state.cells[Math.floor(state.cells.length / 2)]);
}

function buildMatrix(data) {
  for (const c of state.cells) disposeGroup(c.obj);
  state.cells = [];
  const M = data.matrix;
  const nr = M.rows.length, nc = M.cols.length;
  const el = $('#matrix');
  const size = nc > 6 ? 96 : nc > 4 ? 116 : 136;
  el.style.setProperty('--cell-size', `${size}px`);
  el.style.gridTemplateColumns = `22px auto repeat(${nc}, var(--cell-size))`;
  let html = `<div></div><div></div><div class="axis-title" style="grid-column: 3 / span ${nc}">${esc(M.col_title)}</div>`;
  html += `<div></div><div></div>${M.cols.map((c) => `<div class="hdr"><b>${esc(c.label)}</b>${c.detail ? `<span>${esc(c.detail)}</span>` : ''}</div>`).join('')}`;
  const byPos = new Map(data.cells.map((c) => [`${c.row},${c.col}`, c]));
  for (let r = 0; r < nr; r++) {
    if (r === 0) html += `<div class="axis-title rows" style="grid-row: 3 / span ${nr}">${esc(M.row_title)}</div>`;
    html += `<div class="hdr row"><b>${esc(M.rows[r].label)}</b>${M.rows[r].detail ? `<span>${esc(M.rows[r].detail)}</span>` : ''}</div>`;
    for (let c = 0; c < nc; c++) {
      const cd = byPos.get(`${r},${c}`);
      html += cd
        ? `<div class="cell" data-id="${esc(cd.id)}" title="${esc(cd.title || cd.label)}"><span class="lab">${esc(cd.label)}</span>${cd.sub ? `<span class="sub">${esc(cd.sub)}</span>` : ''}</div>`
        : `<div class="cell empty"></div>`;
    }
  }
  el.innerHTML = html;
  let maxR = 0;
  for (const cd of data.cells) {
    const obj = buildCrystal(cd, data, state.color);
    scene.add(obj);
    maxR = Math.max(maxR, obj.userData.radius);
    state.cells.push({ data: cd, obj, el: el.querySelector(`.cell[data-id="${CSS.escape(cd.id)}"]`) });
  }
  state.radius = maxR;
}

function rebuildObjects() {
  for (const c of state.cells) {
    disposeGroup(c.obj);
    c.obj = buildCrystal(c.data, state.data, state.color);
    scene.add(c.obj);
  }
  if (state.selected) selectCell(state.selected, true);
}

function fmt(x, d = 3) { return Number(x).toFixed(d); }

function selectCell(cell, keepView = false) {
  if (!cell) return;
  state.selected?.el?.classList.remove('sel');
  state.selected = cell;
  cell.el?.classList.add('sel');
  const d = cell.data;
  const D = state.data;
  if (state.detail) disposeGroup(state.detail);
  state.detail = buildCrystal(d, D, state.color);
  scene.add(state.detail);
  if (!keepView) {
    detailCam.position.set(0, 0, 10);
    detailCam.zoom = 1;
    detailCam.updateProjectionMatrix();
    controls.target.set(0, 0, 0);
    state.detail.quaternion.copy(DEFAULT_Q);
  }
  $('#d-title').textContent = `${D.name} · ${d.label}`;
  $('#d-sub').innerHTML = d.description || '';
  const m = d.metrics;
  const fr = Object.entries(d.fractions || {}).map(([k, v]) => `${D.forms.find((f) => f.key === k)?.label || k} ${fmt(100 * v, 0)}%`).join(' · ');
  const rows = [
    ['Faces', `${d.geometry.faces.length} (${[...new Set(d.geometry.faces.map((f) => f.form))].map((k) => D.forms.find((f) => f.key === k)?.label).join(' ')})`],
    ['Face area', fr],
    ['Aspect (L/W)', fmt(m.aspect, 2)],
    ['S/V (V = 1)', fmt(m.surface_area, 3)],
    ['R<sub>sv</sub> = 3V/S', fmt(m.rsv, 3)],
    ['Sphericity', fmt(m.sphericity, 3)],
  ];
  $('#d-metrics').innerHTML = rows.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('');
  $('#d-files').innerHTML = `<a class="btn primary" href="${esc(d.files.step)}" download>STEP</a><a class="btn" href="${esc(d.files.stl)}" download>STL</a>`;
  history.replaceState(null, '', `#${D.id}/${d.id}`);
}

function setupDrag() {
  const host = $('#matrix');
  let start = null, last = null, moved = false;
  host.addEventListener('pointerdown', (e) => {
    if (!e.target.closest('.cell:not(.empty)')) return;
    start = last = { x: e.clientX, y: e.clientY };
    moved = false;
    host.setPointerCapture(e.pointerId);
  });
  host.addEventListener('pointermove', (e) => {
    if (!start) return;
    const dx = e.clientX - last.x, dy = e.clientY - last.y;
    last = { x: e.clientX, y: e.clientY };
    if (!moved && Math.hypot(e.clientX - start.x, e.clientY - start.y) > 4) { moved = true; host.classList.add('dragging'); }
    if (moved) {
      const qx = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), dy * 0.01);
      const qy = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), dx * 0.01);
      gridQ.premultiply(qy).premultiply(qx);
    }
  });
  const end = (e) => {
    if (!start) return;
    if (!moved) {
      const cellEl = document.elementFromPoint(e.clientX, e.clientY)?.closest('.cell:not(.empty)');
      const cell = cellEl && state.cells.find((c) => c.el === cellEl);
      if (cell) selectCell(cell);
    }
    start = null;
    host.classList.remove('dragging');
  };
  host.addEventListener('pointerup', end);
  host.addEventListener('pointercancel', () => { start = null; host.classList.remove('dragging'); });
}

// --------------------------------------------------------------- render
function intersect(a, b) {
  const left = Math.max(a.left, b.left), top = Math.max(a.top, b.top);
  const right = Math.min(a.right, b.right), bottom = Math.min(a.bottom, b.bottom);
  return right > left && bottom > top ? { left, top, right, bottom } : null;
}

function drawInto(rect, clip, cam, obj, H) {
  const vis = intersect(rect, clip);
  if (!vis) return;
  const w = rect.right - rect.left, h = rect.bottom - rect.top;
  renderer.setViewport(rect.left, H - rect.bottom, w, h);
  renderer.setScissor(vis.left, H - vis.bottom, vis.right - vis.left, vis.bottom - vis.top);
  const aspect = w / h;
  const s = cam.userData.half || 1;
  cam.left = -s * aspect; cam.right = s * aspect; cam.top = s; cam.bottom = -s;
  cam.updateProjectionMatrix();
  obj.visible = true;
  renderer.render(scene, cam);
  obj.visible = false;
}

const spinQ = new THREE.Quaternion();
const Yaxis = new THREE.Vector3(0, 1, 0);
let prevT = performance.now();

function loop(t) {
  const dt = Math.min(0.05, (t - prevT) / 1000);
  prevT = t;
  const W = window.innerWidth, H = window.innerHeight;
  if (canvas.width !== Math.floor(W * renderer.getPixelRatio()) || canvas.height !== Math.floor(H * renderer.getPixelRatio())) {
    renderer.setSize(W, H, false);
  }
  if (state.spin) spinAngle += dt * 0.45;
  spinQ.setFromAxisAngle(Yaxis, spinAngle);
  const q = gridQ.clone().multiply(spinQ);

  renderer.setScissorTest(false);
  renderer.clear();
  renderer.setScissorTest(true);

  const scrollRect = $('#matrix-scroll').getBoundingClientRect();
  const win = { left: 0, top: 0, right: W, bottom: H };
  const clip = intersect(scrollRect, win);
  if (clip) {
    for (const c of state.cells) {
      if (!c.el) continue;
      const r = c.el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > H) continue;
      c.obj.quaternion.copy(q);
      const rad = state.scale === 'fit' ? c.obj.userData.radius : state.radius;
      gridCam.userData.half = rad * 1.04;
      drawInto(r, clip, gridCam, c.obj, H);
    }
  }
  if (state.detail) {
    controls.update();
    const r = detailEl.getBoundingClientRect();
    detailCam.userData.half = state.detail.userData.radius * 1.12;
    drawInto(r, win, detailCam, state.detail, H);
  }
  requestAnimationFrame(loop);
}

init().catch((err) => {
  console.error(err);
  $('#m-title').textContent = 'Could not load data';
  $('#m-sub').textContent = String(err);
});
