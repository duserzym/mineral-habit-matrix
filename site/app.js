import * as THREE from 'three';
import { GridView, SoloView, crystalObject, viewQ } from './views.js';
import { facesFromJSON } from './geom.js';
import { Learn } from './learn.js';

const $ = (s) => document.querySelector(s);
export const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

const state = {
  index: [], cache: new Map(), data: null, cells: [], selected: null, page: 'matrix',
  spin: true, edges: true, color: 'form', scale: 'fit',
};

async function loadData(id) {
  if (!state.cache.has(id)) {
    const entry = state.index.find((m) => m.id === id);
    state.cache.set(id, fetch(`data/${entry.file}`, { cache: 'no-cache' }).then((r) => r.json()));
  }
  return state.cache.get(id);
}

// ------------------------------------------------------------------ theme
const THEMES = ['auto', 'light', 'dark'];
const ICONS = { auto: '◐', light: '☀', dark: '☾' };
let theme = 'auto';
try { theme = localStorage.getItem('mhm-theme') || 'auto'; } catch { /* storage unavailable */ }
function applyTheme() {
  if (theme === 'auto') delete document.documentElement.dataset.theme;
  else document.documentElement.dataset.theme = theme;
  const b = $('#theme-btn');
  b.textContent = ICONS[theme];
  b.title = `Theme: ${theme}`;
}
applyTheme();

// ------------------------------------------------------------------ views
const grid = new GridView($('#stage'), $('#matrix-scroll'));
const atlasGrid = new GridView($('#atlas-stage'), $('#atlas-stage'));
const sheetView = new SoloView($('#sheet-view'));
const learn = new Learn({ loadData, index: () => state.index });
let DEFAULT_Q = viewQ();
const gridQ = DEFAULT_Q.clone();
let spinAngle = 0;

$('#theme-btn').onclick = () => {
  theme = THEMES[(THEMES.indexOf(theme) + 1) % 3];
  try { localStorage.setItem('mhm-theme', theme); } catch { /* ignore */ }
  applyTheme();
  rebuildObjects();
  learn.refresh();
};

function crystalFor(cell, data) {
  return crystalObject(facesFromJSON(cell.geometry, data), data, { color: state.color, edges: state.edges });
}

// ------------------------------------------------------------------ router
async function route() {
  const parts = location.hash.slice(1).split('/').filter(Boolean).map(decodeURIComponent);
  const valid = (id) => state.index.some((m) => m.id === id);
  closeMenu();
  if (!parts.length || parts[0] === 'atlas') {
    showPage('atlas');
    closeSheet(true);
    return;
  }
  if (parts[0] === 'learn') {
    showPage('learn');
    closeSheet(true);
    const m = valid(parts[1]) ? parts[1] : state.data?.id || state.index[0].id;
    await learn.show(m, parts[2]);
    return;
  }
  const m = valid(parts[0]) ? parts[0] : state.index[0].id;
  showPage('matrix');
  if (state.data?.id !== m) await loadMineral(m);
  showPage('matrix');
  const cell = parts[1] && state.cells.find((c) => c.data.id === parts[1]);
  if (cell) openSheet(cell); else closeSheet();
}

function showPage(p) {
  const changed = state.page !== p;
  state.page = p;
  $('#page-matrix').hidden = p !== 'matrix';
  $('#page-learn').hidden = p !== 'learn';
  $('#page-atlas').hidden = p !== 'atlas';
  $('#learn-tab').classList.toggle('active', p === 'learn');
  $('#atlas-link').classList.toggle('active', p === 'atlas');
  $('#menu-current').textContent = p === 'matrix' && state.data ? state.data.name : 'Minerals';
  renderTabs(p === 'matrix' ? state.data : null);
  if (changed) window.scrollTo(0, 0);
}

// ------------------------------------------------------------------ matrix page
async function loadMineral(id) {
  const data = await loadData(id);
  state.data = data;
  DEFAULT_Q = viewQ(data.view?.tilt, data.view?.turn);
  gridQ.copy(DEFAULT_Q);
  spinAngle = 0;

  $('#m-name').textContent = data.name;
  $('#m-title').textContent = data.matrix.title;
  $('#m-sub').innerHTML = data.matrix.subtitle || '';
  $('#m-note').innerHTML = data.matrix.note || '';
  $('#legend').innerHTML = data.forms.map((f) =>
    `<li><span class="sw" style="background:${f.color}"></span><code>${esc(f.label)}</code>${esc(f.name)}</li>`).join('');

  const L = data.lattice;
  const facts = [
    ['Formula', data.formula], ['Chronometers', data.chronometers],
    ['System', `${data.system} · ${data.point_group}`], ['Setting', data.setting],
    ['Cell', `a ${L.a}, b ${L.b}, c ${L.c} Å · α ${L.alpha}°, β ${L.beta}°, γ ${L.gamma}°`], ['Cell source', data.lattice_source],
  ];
  const habits = (data.habits || []).map((h) => `<li><strong>${esc(h.name)}.</strong> ${h.text}</li>`).join('');
  $('#about-mineral').innerHTML = `<h2>${esc(data.name)}: habits &amp; morphology</h2>
    <dl class="metrics">${facts.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('')}</dl>
    ${data.about || ''}${habits ? `<ul class="habits">${habits}</ul>` : ''}`;
  $('#refs').innerHTML = (data.references || []).map((r) => {
    const link = r.doi ? `<a href="https://doi.org/${esc(r.doi)}" target="_blank" rel="noopener">doi:${esc(r.doi)}</a>`
      : r.url ? `<a href="${esc(r.url)}" target="_blank" rel="noopener">link</a>` : '';
    const tags = (r.tags || []).map((t) => `<span class="tag">${esc(t)}</span>`).join('');
    return `<li>${r.citation} ${link}${tags}<span class="why">${r.note || ''}</span></li>`;
  }).join('');
  buildMatrix(data);
}

function buildMatrix(data) {
  const M = data.matrix;
  const nr = M.rows.length, nc = M.cols.length;
  const el = $('#matrix');
  el.style.gridTemplateColumns = `var(--axis-col, 22px) max-content repeat(${nc}, minmax(var(--cell-min, 92px), 1fr))`;
  el.style.maxWidth = `${nc * 230 + 240}px`;
  let html = `<div></div><div></div><div class="axis-title" style="grid-column: 3 / span ${nc}">${esc(M.col_title)}</div>`;
  html += `<div></div><div></div>${M.cols.map((c) => `<div class="hdr"><b>${esc(c.label)}</b>${c.detail ? `<span>${esc(c.detail)}</span>` : ''}</div>`).join('')}`;
  const byPos = new Map(data.cells.map((c) => [`${c.row},${c.col}`, c]));
  for (let r = 0; r < nr; r++) {
    if (r === 0) html += `<div class="axis-title rows" style="grid-row: 3 / span ${nr}">${esc(M.row_title)}</div>`;
    html += `<div class="hdr row"><b>${esc(M.rows[r].label)}</b>${M.rows[r].detail ? `<span>${esc(M.rows[r].detail)}</span>` : ''}</div>`;
    for (let c = 0; c < nc; c++) {
      const cd = byPos.get(`${r},${c}`);
      html += cd
        ? `<div class="cell" data-id="${esc(cd.id)}" title="${esc(cd.title || cd.description || cd.label)}" role="button" tabindex="0" aria-label="${esc(data.name)} ${esc(cd.label)}"><span class="lab">${esc(cd.label)}</span><div class="view"></div></div>`
        : `<div class="cell empty"></div>`;
    }
  }
  el.innerHTML = html;
  state.selected = null;
  state.cells = data.cells.map((cd) => {
    const cellEl = el.querySelector(`.cell[data-id="${CSS.escape(cd.id)}"]`);
    return { data: cd, el: cellEl, view: cellEl.querySelector('.view'), obj: crystalFor(cd, data) };
  });
  grid.setItems(state.cells.map((c) => ({ el: c.view, obj: c.obj })));
  const rowHdr = el.querySelector('.hdr.row');
  grid.stickyLeft = () => rowHdr?.getBoundingClientRect().right;
  for (const c of state.cells) {
    c.el.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(c); } });
  }
}

function rebuildObjects() {
  if (!state.data) return;
  for (const c of state.cells) c.obj = crystalFor(c.data, state.data);
  grid.setItems(state.cells.map((c) => ({ el: c.view, obj: c.obj })));
  if (state.selected && $('#sheet').classList.contains('open')) showInSheet(state.selected, true);
}

function select(cell) {
  location.hash = `#${state.data.id}/${encodeURIComponent(cell.data.id)}`;
}

// ------------------------------------------------------------------ inspector
const fmt = (x, d = 3) => Number(x).toFixed(d);

function showInSheet(cell, keepView = false) {
  const D = state.data, d = cell.data;
  const obj = crystalFor(d, D);
  sheetView.set(obj, obj.userData.radius, keepView ? null : DEFAULT_Q);
  if (!keepView) sheetView.resetView();
  $('#s-mineral').textContent = D.name;
  $('#s-title').textContent = d.label;
  $('#s-desc').innerHTML = d.description || '';
  const forms = D.forms.filter((f) => d.fractions[f.key] != null);
  $('#s-facebar').innerHTML = forms.map((f) => `<span style="width:${100 * d.fractions[f.key]}%;background:${f.color}" title="${esc(f.label)} ${fmt(100 * d.fractions[f.key], 1)}%"></span>`).join('');
  $('#s-legend').innerHTML = forms.map((f) => `<li><span class="sw" style="background:${f.color}"></span><code>${esc(f.label)}</code>${fmt(100 * d.fractions[f.key], 0)}%</li>`).join('');
  const m = d.metrics;
  const nFaces = (k) => d.geometry.faces.filter((f) => f.form === k).length;
  const rows = [
    ['Faces', `${d.geometry.faces.length} = ${forms.map((f) => `${nFaces(f.key)}×${f.label}`).join(' + ')}`],
    ['Aspect (L/W)', fmt(m.aspect, 2)],
    ['Surface (V = 1)', fmt(m.surface_area, 3)],
    ['R<sub>sv</sub> = 3V/S', fmt(m.rsv, 3)],
    ['Sphericity', fmt(m.sphericity, 3)],
  ];
  $('#s-metrics').innerHTML = rows.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('');
  $('#s-learn').href = `#learn/${D.id}/${encodeURIComponent(d.id)}`;
  $('#s-step').href = d.files.step;
  $('#s-stl').href = d.files.stl;
}

function openSheet(cell) {
  state.selected?.el?.classList.remove('sel');
  state.selected = cell;
  cell.el.classList.add('sel');
  const sh = $('#sheet');
  sh.hidden = false;
  showInSheet(cell);
  requestAnimationFrame(() => sh.classList.add('open'));
}

function closeSheet(immediate = false) {
  const sh = $('#sheet');
  state.selected?.el?.classList.remove('sel');
  sh.classList.remove('open');
  if (immediate) sh.hidden = true;
  else setTimeout(() => { if (!sh.classList.contains('open')) sh.hidden = true; }, 380);
}

$('#sheet-close').onclick = () => { location.hash = `#${state.data.id}`; };
// phones: swipe the inspector sheet down to close it
{
  let y0 = null;
  const sh = $('#sheet');
  sh.addEventListener('touchstart', (e) => { y0 = e.target.closest('.sheet-view') ? null : e.touches[0].clientY; }, { passive: true });
  sh.addEventListener('touchmove', (e) => {
    if (y0 == null || sh.scrollTop > 0) return;
    const dy = e.touches[0].clientY - y0;
    if (dy > 0) sh.style.transform = `translateY(${dy}px)`;
  }, { passive: true });
  sh.addEventListener('touchend', (e) => {
    if (y0 == null) return;
    const dy = e.changedTouches[0].clientY - y0;
    sh.style.transform = '';
    y0 = null;
    if (dy > 90) location.hash = `#${state.data.id}`;
  });
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && $('#sheet').classList.contains('open')) location.hash = `#${state.data.id}`;
});

// ------------------------------------------------------------------ controls
function setToggle(btn, on) { btn.classList.toggle('on', on); btn.setAttribute('aria-pressed', String(on)); }
$('#opt-rotate').onclick = (e) => { state.spin = !state.spin; setToggle(e.currentTarget, state.spin); };
$('#opt-edges').onclick = (e) => {
  state.edges = !state.edges;
  setToggle(e.currentTarget, state.edges);
  for (const c of state.cells) c.obj.userData.edges.visible = state.edges;
  const so = sheetView.root.children[0];
  if (so?.userData.edges) so.userData.edges.visible = state.edges;
};
for (const b of document.querySelectorAll('[data-scale]')) {
  b.onclick = () => {
    state.scale = grid.scaleMode = b.dataset.scale;
    document.querySelectorAll('[data-scale]').forEach((x) => x.classList.toggle('on', x === b));
  };
}
for (const b of document.querySelectorAll('[data-color]')) {
  b.onclick = () => {
    state.color = b.dataset.color;
    document.querySelectorAll('[data-color]').forEach((x) => x.classList.toggle('on', x === b));
    rebuildObjects();
  };
}
$('#opt-reset').onclick = () => { gridQ.copy(DEFAULT_Q); spinAngle = 0; };

function setupDrag() {
  const host = $('#matrix');
  let start = null, last = null, moved = false;
  host.addEventListener('pointerdown', (e) => {
    if (!e.target.closest('.cell:not(.empty)') || e.button !== 0) return;
    start = last = { x: e.clientX, y: e.clientY };
    moved = false;
  });
  window.addEventListener('pointermove', (e) => {
    if (!start) return;
    const dx = e.clientX - last.x, dy = e.clientY - last.y;
    last = { x: e.clientX, y: e.clientY };
    if (!moved && Math.hypot(e.clientX - start.x, e.clientY - start.y) > 5) { moved = true; host.classList.add('dragging'); }
    if (moved) {
      gridQ.premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), dx * 0.01))
        .premultiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), dy * 0.01));
    }
  });
  window.addEventListener('pointerup', (e) => {
    if (!start) return;
    if (!moved) {
      const cellEl = e.target.closest?.('.cell:not(.empty)');
      const cell = cellEl && state.cells.find((c) => c.el === cellEl);
      if (cell) select(cell);
    }
    start = null;
    host.classList.remove('dragging');
  });
  window.addEventListener('pointercancel', () => { start = null; host.classList.remove('dragging'); });
}

// ------------------------------------------------------------------ navigation
const groupsOf = () => {
  const g = new Map();
  for (const m of state.index) { if (!g.has(m.group)) g.set(m.group, []); g.get(m.group).push(m); }
  return g;
};

function renderTabs(current) {
  const tabs = $('#tabs');
  if (!current) { tabs.innerHTML = ''; return; }
  const sibs = state.index.filter((m) => m.group === current.group);
  tabs.innerHTML = sibs.map((m) => `<button class="tab" type="button" role="tab" data-id="${esc(m.id)}" aria-selected="${m.id === current.id}">${esc(m.name)}</button>`).join('');
  for (const b of tabs.querySelectorAll('.tab')) b.onclick = () => { location.hash = `#${b.dataset.id}`; };
  tabs.querySelector('[aria-selected="true"]')?.scrollIntoView({ block: 'nearest', inline: 'nearest' });
}

function buildMenu() {
  $('#menu-groups').innerHTML = [...groupsOf()].map(([g, ms]) => `<div class="menu-group"><h4>${esc(g)}</h4>${ms.map((m) =>
    `<button class="menu-item" type="button" role="menuitem" data-id="${esc(m.id)}" data-q="${esc(`${m.name} ${m.formula} ${m.group} ${m.chronometers} ${m.system}`.toLowerCase())}">${esc(m.name)}<small>${esc(m.formula)}</small></button>`).join('')}</div>`).join('');
  for (const b of document.querySelectorAll('.menu-item')) b.onclick = () => { location.hash = `#${b.dataset.id}`; closeMenu(); };
  $('#menu-btn').onclick = (e) => { e.stopPropagation(); $('#mineral-menu').hidden ? openMenu() : closeMenu(); };
  $('#menu-search').oninput = (e) => {
    const q = e.target.value.trim().toLowerCase();
    for (const b of document.querySelectorAll('.menu-item')) b.hidden = q && !b.dataset.q.includes(q);
    for (const g of document.querySelectorAll('.menu-group')) g.hidden = ![...g.querySelectorAll('.menu-item')].some((b) => !b.hidden);
  };
  $('#menu-search').onkeydown = (e) => {
    if (e.key === 'Enter') document.querySelector('.menu-item:not([hidden])')?.click();
  };
  document.addEventListener('click', (e) => { if (!e.target.closest('#mineral-menu, #menu-btn')) closeMenu(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });
}

function openMenu() {
  const m = $('#mineral-menu');
  m.hidden = false;
  $('#menu-btn').setAttribute('aria-expanded', 'true');
  for (const b of document.querySelectorAll('.menu-item')) b.classList.toggle('current', state.page === 'matrix' && b.dataset.id === state.data?.id);
  $('#menu-search').value = '';
  $('#menu-search').dispatchEvent(new Event('input'));
  $('#menu-search').focus();
}

function closeMenu() {
  $('#mineral-menu').hidden = true;
  $('#menu-btn').setAttribute('aria-expanded', 'false');
}

async function buildAtlas() {
  const atlas = await (await fetch('data/atlas.json', { cache: 'no-cache' })).json();
  $('#atlas-groups').innerHTML = [...groupsOf()].map(([g, ms]) => `<section class="atlas-group"><h2>${esc(g)}</h2><div class="atlas-cards">${ms.map((m) =>
    `<a class="atlas-card glass" href="#${esc(m.id)}" data-id="${esc(m.id)}" data-q="${esc(`${m.name} ${m.formula} ${m.group} ${m.chronometers} ${m.system} ${m.matrix_title}`.toLowerCase())}">
      <span class="n">${m.ncells}</span><div class="view"></div><h3>${esc(m.name)}</h3>
      <div class="f">${esc(m.formula)} · ${esc(m.system)}</div>${m.chronometers ? `<div class="c">${esc(m.chronometers)}</div>` : ''}</a>`).join('')}</div></section>`).join('');
  const items = [];
  for (const card of document.querySelectorAll('.atlas-card')) {
    const pv = atlas[card.dataset.id];
    if (!pv) continue;
    const pseudo = { forms: pv.forms.map((f) => ({ ...f, label: f.key })), mono_color: pv.mono_color };
    const obj = crystalObject(facesFromJSON(pv.geometry, pseudo), pseudo, { edges: true });
    items.push({ el: card.querySelector('.view'), obj, q: viewQ(pv.view?.tilt, pv.view?.turn) });
  }
  atlasGrid.setItems(items);
  const count = () => {
    const n = [...document.querySelectorAll('.atlas-card')].filter((c) => !c.hidden).length;
    $('#atlas-count').textContent = `${n} minerals · ${state.index.reduce((s, m) => s + m.ncells, 0)} crystals`;
  };
  $('#atlas-search').oninput = (e) => {
    const q = e.target.value.trim().toLowerCase();
    for (const c of document.querySelectorAll('.atlas-card')) c.hidden = q && !c.dataset.q.includes(q);
    for (const g of document.querySelectorAll('.atlas-group')) g.hidden = ![...g.querySelectorAll('.atlas-card')].some((c) => !c.hidden);
    count();
  };
  count();
}

// ------------------------------------------------------------------ loop
const spinQ = new THREE.Quaternion();
const Y = new THREE.Vector3(0, 1, 0);
let prevT = performance.now();
function loop(t) {
  const dt = Math.min(0.05, (t - prevT) / 1000);
  prevT = t;
  if (state.page === 'matrix') {
    if (state.spin) spinAngle += dt * 0.45;
    spinQ.setFromAxisAngle(Y, spinAngle);
    grid.q.copy(gridQ).multiply(spinQ);
    grid.frame();
    if ($('#sheet').classList.contains('open')) sheetView.frame();
  } else if (state.page === 'atlas') {
    if (state.spin) spinAngle += dt * 0.45;
    spinQ.setFromAxisAngle(Y, spinAngle);
    for (const it of atlasGrid.items) it.obj.quaternion.copy(it.q).multiply(spinQ);
    atlasGrid.frame();
  } else {
    learn.frame();
  }
  requestAnimationFrame(loop);
}

async function init() {
  state.index = await (await fetch('data/index.json', { cache: 'no-cache' })).json();
  buildMenu();
  await buildAtlas();
  setupDrag();
  window.addEventListener('hashchange', () => route().catch(console.error));
  await route();
  requestAnimationFrame(loop);
}

init().catch((err) => {
  console.error(err);
  $('#m-title').textContent = 'Could not load data';
  $('#m-sub').textContent = String(err);
});
