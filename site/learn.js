// Step-by-step reconstruction of any crystal in the matrix, from lattice to exported solid.
import * as THREE from 'three';
import {
  SoloView, crystalObject, cellFrame, vectorArrow, viewQ, inCrystalFrame, planeDiscs, fade, symmetryElement, dispose,
} from './views.js';
import {
  planesFor, solidFrom, formAreas, effectiveDistances, volume, aspect, radius, dot, len, angle, fmtIndex, mul,
  add, sub, cross, unit, apply, symmetryStages, partialOp,
} from './geom.js';

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const f3 = (x, d = 3) => Number(x).toFixed(d);
const vec = (v, d = 3) => `(${v.map((x) => f3(x, d)).join(', ')})`;
const paren = (idx) => `(${fmtIndex(idx)})`;
const AXIS_COLORS = ['#e5484d', '#30a46c', '#0090ff'];
const ease = (s) => (s < 0.5 ? 2 * s * s : 1 - (-2 * s + 2) ** 2 / 2);
const motion = () => (matchMedia('(prefers-reduced-motion: reduce)').matches ? 0.02 : 1);

/** Name of a symmetry direction in the Cartesian frame (a ∥ x, b ∥ y, c ∥ z wherever the axes are orthogonal). */
function axisName(v) {
  const a = v.map(Math.abs);
  if (a[2] > 0.9999) return 'c';
  if (a[1] > 0.9999) return 'b';
  if (a[0] > 0.9999) return 'a';
  if (Math.abs(a[0] - a[1]) < 1e-6 && Math.abs(a[1] - a[2]) < 1e-6) return 'the body diagonal [111]';
  if (a[2] < 1e-6 && Math.abs(a[0] - Math.sqrt(3) / 2) < 1e-6) return 'a₁';
  return vec(v, 2);
}

/** Outward-wound copy of a face after moving its vertices (so front-face culling still works). */
function movedFace(f, loop, towards) {
  let s = [0, 0, 0];
  for (let i = 1; i < loop.length - 1; i++) s = add(s, cross(sub(loop[i], loop[0]), sub(loop[i + 1], loop[0])));
  const flip = dot(s, towards) < 0;
  const n = len(s) > 1e-12 ? unit(flip ? mul(s, -1) : s) : unit(towards);
  return { ...f, n, loop: flip ? [...loop].reverse() : loop };
}

export class Learn {
  constructor({ loadData, index }) {
    this.loadData = loadData;
    this.index = index;
    this.view = new SoloView($('#learn-view'));
    this.step = 0;
    this.data = null;
    this.cell = null;
    $('#learn-prev').onclick = () => this.go(this.step - 1);
    $('#learn-next').onclick = () => this.go(this.step + 1);
    $('#learn-mineral').onchange = (e) => { location.hash = `#learn/${e.target.value}`; };
    $('#learn-cell').onchange = (e) => { location.hash = `#learn/${this.data.id}/${encodeURIComponent(e.target.value)}`; };
    document.addEventListener('keydown', (e) => {
      if ($('#page-learn').hidden || e.target.closest?.('input, select, textarea')) return;
      if (e.key === 'ArrowRight') this.go(this.step + 1);
      if (e.key === 'ArrowLeft') this.go(this.step - 1);
    });
  }

  async show(mineralId, cellId) {
    const data = await this.loadData(mineralId);
    const cell = data.cells.find((c) => c.id === cellId) || data.cells.find((c) => c.default) || data.cells[0];
    const sameCrystal = this.data?.id === data.id && this.cell?.id === cell.id;
    this.data = data;
    this.cell = cell;
    $('#learn-mineral').innerHTML = this.index().map((m) => `<option value="${esc(m.id)}"${m.id === data.id ? ' selected' : ''}>${esc(m.name)}</option>`).join('');
    $('#learn-cell').innerHTML = data.cells.map((c) => `<option value="${esc(c.id)}"${c.id === cell.id ? ' selected' : ''}>${esc(c.label)}${c.title && c.title !== c.label ? ` · ${esc(c.title.replace(`${c.label}: `, ''))}` : ''}</option>`).join('');
    $('#learn-back').href = `#${data.id}/${encodeURIComponent(cell.id)}`;
    if (!sameCrystal) {
      this.prepare();
      this.renderSteps();
      this.go(0, true);
    }
  }

  /** Everything the steps need, computed once per crystal. */
  prepare() {
    const D = this.data, C = this.cell;
    this.present = D.forms.filter((f) => C.params.planes[f.key] != null);
    // prisms first (normals perpendicular to the axis), then terminations
    const u = D.axis;
    this.order = [...this.present].sort((a, b) => (u ? Math.abs(dot(a.normals[0], u)) - Math.abs(dot(b.normals[0], u)) : 0));
    this.final = solidFrom(planesFor(D, C.params.planes));
    this.R = radius(this.final);
    this.q = viewQ(D.view?.tilt, D.view?.turn);
    this.cut = 1;
    this.stages = symmetryStages(this.present, D.point_group);
    this.symAt = this.stages.length;
    this.live = {
      dist: Object.fromEntries(D.forms.map((f) => [f.key, C.params.face_distances[f.key] ?? null])),
      on: Object.fromEntries(D.forms.map((f) => [f.key, C.params.face_distances[f.key] != null])),
      t: C.params.cap_translation,
    };
    this.view.resetView(this.q);
  }

  legend(forms) {
    $('#learn-legend').innerHTML = forms.map((f) => `<li><span class="sw" style="background:${f.color}"></span><code>${esc(f.label)}</code></li>`).join('');
  }

  steps() {
    const D = this.data, C = this.cell, L = D.lattice, R = this.R;
    const ghost = () => crystalObject(this.final, D, { opacity: 0.16, edges: true });
    const A = D.basis, Rs = D.reciprocal;
    const p = C.params;
    const u = D.axis;
    const nameOf = (k) => D.forms.find((f) => f.key === k);

    return [
      {
        title: 'Start from the unit cell',
        fitR: 1.3,
        scene: () => [ghost(), inCrystalFrame(cellFrame(A, R))],
        body: () => `
          <p>A crystal's faces are planes of its lattice, so everything starts with the unit cell. ${esc(D.name)} is
          <strong>${esc(D.system.toLowerCase())}</strong>, point group <strong>${esc(D.point_group)}</strong>, in the setting ${esc(D.setting)}.</p>
          <table><tr><th>a</th><th>b</th><th>c</th><th>α</th><th>β</th><th>γ</th></tr>
          <tr><td class="num">${L.a} Å</td><td class="num">${L.b} Å</td><td class="num">${L.c} Å</td><td class="num">${L.alpha}°</td><td class="num">${L.beta}°</td><td class="num">${L.gamma}°</td></tr></table>
          <p>To work in Cartesian space we place <strong>c along z</strong> and <strong>b in the yz-plane</strong>. The dashed box is the cell,
          scaled up and centred on the crystal (shown as a ghost). Source of the cell: ${D.lattice_source || '—'}.</p>
          <div class="formula">a = ${vec(A[0], 3)}<br>b = ${vec(A[1], 3)}<br>c = ${vec(A[2], 3)}</div>`,
      },
      {
        title: 'Turn Miller indices into face normals',
        fitR: 1.65,
        scene: () => {
          const objs = [];
          const m = Math.max(...Rs.map(len));
          ['a*', 'b*', 'c*'].forEach((n, i) => objs.push(vectorArrow(mul(Rs[i], (0.9 * R) / m), AXIS_COLORS[i], n, R, { head: 0.08 })));
          for (const f of this.present) objs.push(vectorArrow(mul(f.normals[0], 1.45 * R), f.color, paren(f.hkls[0]), R));
          return [ghost(), inCrystalFrame(...objs)];
        },
        body: () => {
          const rows = this.present.map((f) => {
            const n = f.normals[0];
            const ang = u ? `${f3(angle(n, u), 1)}°` : '—';
            return `<tr><td><span class="sw" style="background:${f.color};display:inline-block;vertical-align:-1px"></span> ${esc(paren(f.hkls[0]))}</td><td class="num">${vec(n, 3)}</td><td class="num">${ang}</td></tr>`;
          }).join('');
          const pair = this.present.length > 1
            ? `<p>Because these directions come from the real cell, the angle between faces is fixed by the lattice. For example
               ${esc(paren(this.present[0].hkls[0]))} ∧ ${esc(paren(this.present[this.present.length - 1].hkls[0]))} = <strong>${f3(angle(this.present[0].normals[0], this.present[this.present.length - 1].normals[0]), 2)}°</strong>.
               A different c/a would give different angles and a visibly different crystal, even with the same faces.</p>` : '';
          return `
          <p>The plane (hkl) is perpendicular to the <strong>reciprocal-lattice</strong> vector</p>
          <div class="formula">n<sub>hkl</sub> = h a* + k b* + l c*,&nbsp;&nbsp; a* = (b × c)/V, b* = (c × a)/V, c* = (a × b)/V</div>
          <p>The coloured arrows are the normals of one face of each form in this crystal${D.system === 'Hexagonal' || D.system === 'Trigonal' ? ' (Miller–Bravais (hkil) with i dropped)' : ''}. The red, green and blue arrows are a*, b* and c*.</p>
          <table><tr><th>face</th><th>unit normal</th><th>angle to ${u ? 'axis' : '—'}</th></tr>${rows}</table>${pair}`;
        },
      },
      {
        title: 'Symmetry completes each form',
        fitR: 1.45,
        scene: () => {
          this.symRoot = new THREE.Group();
          this.symDrawn = null;
          return [crystalObject(this.final, D, { opacity: 0.12, edges: true }), this.symRoot];
        },
        body: () => {
          const rows = this.present.map((f) => `<tr><td><span class="sw" style="background:${f.color};display:inline-block;vertical-align:-1px"></span> ${esc(f.label)}</td><td class="num">${f.normals.length}</td><td class="num">${f.hkls.slice(0, 6).map((h) => esc(paren(h))).join(' ')}${f.hkls.length > 6 ? ' …' : ''}</td></tr>`).join('');
          const pills = [`<button class="pill" data-sym="0" type="button">One face each</button>`]
            .concat(this.stages.map((st, i) => `<button class="pill" data-sym="${i + 1}" type="button">+ ${esc(st.op.symbol)}${st.op.axis ? ` ∥ ${esc(axisName(st.op.axis))}` : st.op.normal ? ` ⊥ ${esc(axisName(st.op.normal))}` : ''}</button>`))
            .join('');
          return `
          <p>The point group <strong>${esc(D.point_group)}</strong> has ${D.pg_order} symmetry operations, all generated by
          ${this.stages.length ? `a few <em>symmetry elements</em>` : 'the identity alone'}. Start from one face of each form and let the
          elements copy it: every copy is another face of the same <em>form</em> {hkl}, at the <strong>same distance</strong> from the
          centre. That is why real crystals look symmetric, and why one choice per form fixes all of its faces.</p>
          <div class="sub-steps">${pills}<button class="pill" data-play type="button">▶ Replay</button></div>
          <p data-symtext class="sym-text"></p>
          <table><tr><th>form</th><th>faces</th><th>indices</th></tr>${rows}</table>
          <p class="muted">Arrows are face normals. A copy whose plane misses the finished crystal still counts as part of the form but leaves
          no face, so it shows as an arrow only. ${this.present.reduce((s, f) => s + f.normals.length, 0)} planes in total.</p>`;
        },
        bind: (el, { entered }) => {
          el.querySelectorAll('[data-sym]').forEach((b) => {
            b.onclick = (e) => {
              e.stopPropagation();
              const k = +b.dataset.sym;
              if (k === 0) { this.anim = null; this.symAt = 0; this.symBuild(0, 0, null); } else this.playSym(k - 1, k);
            };
          });
          el.querySelector('[data-play]').onclick = (e) => { e.stopPropagation(); this.playSym(0, this.stages.length); };
          if (entered) this.playSym(0, this.stages.length);
          else this.symBuild(this.symAt, 0, this.symAt > 0 && this.symAt < this.stages.length ? this.symAt - 1 : null);
        },
      },
      {
        title: 'Cut space with half-spaces',
        fitR: 1.6,
        scene: () => {
          const keys = this.order.slice(0, this.cut).map((f) => f.key);
          const faces = solidFrom(planesFor(D, p.planes, keys), 1.5 * R);
          this.legend(this.order.slice(0, this.cut));
          return [crystalObject(faces, D, { highlight: keys[keys.length - 1] })];
        },
        body: () => {
          const keys = this.order.slice(0, this.cut).map((f) => f.key);
          const faces = solidFrom(planesFor(D, p.planes, keys), 1.5 * R);
          const open = faces.some((f) => f.form === 'box');
          const newest = this.order[this.cut - 1];
          const nNew = faces.filter((f) => f.form === newest.key).length;
          const buttons = this.order.map((f, i) => `<button class="pill${i + 1 === this.cut ? ' on' : ''}" data-cut="${i + 1}" type="button"><span class="sw" style="background:${f.color}"></span>+ ${esc(f.label)}</button>`).join('');
          return `
          <p>Each face is a plane <code>n·x = d</code>. The crystal is the region on the inner side of <em>all</em> of them:
          the intersection of the half-spaces <code>n·x ≤ d</code>. This is the Gibbs–Wulff construction. Add the forms one at a time:</p>
          <div class="sub-steps">${buttons}</div>
          <p>Adding <strong>${esc(newest.label)}</strong> (${esc(newest.name)}) at d = ${f3(p.planes[newest.key], 3)} leaves
          <strong>${nNew}</strong> of its ${newest.normals.length} faces on the solid${nNew < newest.normals.length ? '. The rest lie outside and never touch it' : ''}.
          ${open ? 'The solid is still <strong>open</strong>: the blue glass marks directions with no face yet (a prism alone is unbounded along its axis).' : 'The solid is now <strong>closed</strong>.'}
          </p>
          <p class="muted">A plane that misses the solid simply leaves no face. That is how forms appear and disappear across a typology grid.
          The translucent discs are the new planes moving in from outside until they reach their distance d.</p>`;
        },
        bind: (el, { entered }) => {
          el.querySelectorAll('[data-cut]').forEach((b) => {
            b.onclick = (e) => { e.stopPropagation(); this.cut = +b.dataset.cut; this.go(this.step, true); this.sweepCut(); };
          });
          if (entered) this.sweepCut();
        },
        enter: () => { if (this.cut < 1) this.cut = 1; },
      },
      {
        title: 'Relative development sets the distances',
        scene: () => {
          const { faces } = this.liveSolid();
          return [crystalObject(faces, D)];
        },
        body: () => {
          const sliders = D.forms.map((f) => {
            const d = this.live.dist[f.key] ?? this.defaultDist(f.key);
            return `<div class="slider"><label class="lbl"><input type="checkbox" data-on="${f.key}"${this.live.on[f.key] ? ' checked' : ''}>
              <span class="sw" style="background:${f.color}"></span>${esc(f.label)}</label>
              <input type="range" min="-1" max="1" step="0.005" value="${Math.log10(d / this.refDist())}" data-d="${f.key}" aria-label="central distance of ${esc(f.label)}"${this.live.on[f.key] ? '' : ' disabled'}>
              <output data-o="${f.key}">${f3(d, 3)}</output></div>`;
          }).join('');
          const tSlider = u ? `<div class="slider"><span class="lbl">elongation t</span>
              <input type="range" min="0" max="${Math.max(4, 2.5 * p.cap_translation)}" step="0.01" value="${this.live.t}" data-t aria-label="cap translation t">
              <output data-o="t">${f3(this.live.t, 2)}</output></div>` : '';
          return `
          <p>Typologies describe <em>how strongly</em> each form is developed, not where its faces are. This crystal is defined as:</p>
          <div class="formula" style="white-space:normal">${C.description || esc(C.label)}</div>
          <p>The generator turns those ratios into central distances by bisection. Prism ratios become shares of the cross-section perimeter,
          and termination ratios become shares of face area. Move a face outward and its share shrinks until it vanishes; move it inward and
          it takes over. Try it:</p>
          ${sliders}${tSlider}
          <div class="facebar" data-bar style="margin:10px 0 6px"></div>
          <p data-stats class="muted" style="font-size:12.5px"></p>
          <button class="pill" type="button" data-reset>Reset to ${esc(C.label)}</button>`;
        },
        bind: (el) => {
          // k: the form whose slider is moving ('t' for elongation); its planes are drawn as translucent discs
          const refresh = (k = null, override = {}) => {
            const { faces, open, planes, s } = this.liveSolid(override);
            const r = Math.max(radius(faces.filter((f) => f.form !== 'box')), 1e-3);
            const objs = [crystalObject(faces, D)];
            this.discs = null;
            if (k) {
              const color = Object.fromEntries(D.forms.map((f) => [f.key, f.color]));
              const sel = planes.filter((q) => (k === 't' ? Math.abs(dot(q.n, u)) > 1e-6 : q.form === k));
              this.discs = planeDiscs(sel.map((q) => ({ n: q.n, d: q.d * s, color: color[q.form] })), 0.72 * r, { opacity: 0.22 });
              objs.push(this.discs);
            }
            this.view.set(objs, Math.max(radius(faces), 1e-3) * 1.3);
            const areas = formAreas(faces);
            const tot = Object.values(areas).reduce((a, b) => a + b, 0);
            el.querySelector('[data-bar]').innerHTML = D.forms.filter((f) => areas[f.key]).map((f) => `<span style="width:${(100 * areas[f.key]) / tot}%;background:${f.color}"></span>`).join('');
            el.querySelector('[data-stats]').innerHTML = open
              ? 'The solid is open: switch on a termination form or move faces inward.'
              : `${faces.length} faces · ${D.forms.filter((f) => areas[f.key]).map((f) => `${esc(f.label)} ${f3((100 * areas[f.key]) / tot, 0)}%`).join(' · ')} · aspect ${f3(aspect(faces, D.measure_axis || u), 2)}`;
            this.legend(D.forms.filter((f) => areas[f.key]));
          };
          // after a slider is let go, the planes fade out and leave the cut crystal
          const release = () => {
            const discs = this.discs, t0 = performance.now(), T = 900 * motion();
            this.anim = (t) => {
              const a = 1 - (t - t0) / T;
              if (a > 0) { fade(discs, a); return true; }
              dispose(discs);
              return false;
            };
          };
          el.querySelectorAll('[data-d]').forEach((s) => {
            s.oninput = () => {
              const k = s.dataset.d;
              this.anim = null;
              this.live.dist[k] = this.refDist() * 10 ** +s.value;
              el.querySelector(`[data-o="${k}"]`).textContent = f3(this.live.dist[k], 3);
              refresh(k);
            };
            s.onchange = release;
          });
          el.querySelectorAll('[data-on]').forEach((c) => {
            c.onchange = () => {
              const k = c.dataset.on;
              this.live.on[k] = c.checked;
              if (c.checked && this.live.dist[k] == null) this.live.dist[k] = this.defaultDist(k);
              el.querySelector(`[data-d="${k}"]`).disabled = !c.checked;
              if (!c.checked) { this.anim = null; refresh(); return; }
              // switching a form on: its planes come in from outside, cut, then fade
              const d = this.live.dist[k], t0 = performance.now(), T = 1300 * motion();
              this.anim = (t) => {
                const e = Math.min(1, (t - t0) / T);
                refresh(k, { [k]: d * (1 + 0.8 * (1 - ease(e))) });
                if (e < 1) return true;
                release();
                return true;
              };
            };
          });
          const ts = el.querySelector('[data-t]');
          if (ts) {
            ts.oninput = () => { this.anim = null; this.live.t = +ts.value; el.querySelector('[data-o="t"]').textContent = f3(this.live.t, 2); refresh('t'); };
            ts.onchange = release;
          }
          el.querySelector('[data-reset]').onclick = () => {
            this.live.dist = Object.fromEntries(D.forms.map((f) => [f.key, p.face_distances[f.key] ?? null]));
            this.live.on = Object.fromEntries(D.forms.map((f) => [f.key, p.face_distances[f.key] != null]));
            this.live.t = p.cap_translation;
            this.go(this.step, true);
          };
          refresh();
        },
      },
      {
        title: 'Elongate, normalize and export',
        fitR: 1.35,
        scene: () => {
          const objs = [crystalObject(this.final, D)];
          if (u) objs.push(inCrystalFrame(vectorArrow(mul(u, 2.5 * R), '#8e8e93', 'u', R, { from: mul(u, -1.25 * R), head: 0.06 })));
          return objs;
        },
        body: () => {
          const m = C.metrics;
          const rows = this.present.map((f) => {
            const shift = u ? Math.abs(dot(f.normals[0], u)) : 0;
            return `<tr><td><span class="sw" style="background:${f.color};display:inline-block;vertical-align:-1px"></span> ${esc(f.label)}</td><td class="num">${f3(p.face_distances[f.key], 3)}</td><td class="num">${f3(shift, 3)}</td><td class="num">${f3(p.planes[f.key], 4)}</td></tr>`;
          }).join('');
          return `
          ${u ? `<p>Elongation is a rigid translation of the two terminations along the axis u by t, applied as
          <code>d′ = d + |n·u|·t</code>. Prism faces (n ⊥ u) do not move, so the terminations keep their shape. Here t = <strong>${f3(p.cap_translation, 3)}</strong>.</p>` : '<p>This mineral is equant, so there is no elongation step.</p>'}
          <p>Last, everything is scaled by s = <strong>${f3(p.scale, 4)}</strong> so the crystal has <strong>unit volume</strong>, because grain size is not modelled:</p>
          <table><tr><th>form</th><th>d</th><th>|n·u|</th><th>s·(d + |n·u|t)</th></tr>${rows}</table>
          <dl class="metrics"><dt>Volume</dt><dd>${f3(volume(this.final), 4)}</dd><dt>Aspect (L/W)</dt><dd>${f3(m.aspect, 2)}</dd>
          <dt>Surface</dt><dd>${f3(m.surface_area, 3)}</dd><dt>R<sub>sv</sub> = 3V/S</dt><dd>${f3(m.rsv, 3)}</dd><dt>Sphericity</dt><dd>${f3(m.sphericity, 3)}</dd></dl>
          <p>The same half-spaces are written as an exact planar B-rep <strong>STEP</strong> file, with each face named by its Miller index,
          and as a triangulated <strong>STL</strong>.</p>
          <div class="sheet-actions"><a class="pill primary" href="${esc(C.files.step)}" download>Download STEP</a><a class="pill" href="${esc(C.files.stl)}" download>STL</a>
          <a class="pill" href="#${esc(D.id)}/${encodeURIComponent(C.id)}">Back to the matrix</a></div>`;
        },
      },
    ];
  }

  refDist() {
    const k = this.order[0]?.key;
    return this.cell.params.face_distances[k] || 1;
  }

  defaultDist(k) {
    const vals = Object.values(this.cell.params.face_distances).filter((x) => x != null);
    return vals.length ? Math.max(...vals) * 1.05 : 1;
  }

  /** The step-5 solid from the slider state (`override` replaces some central distances), scaled to unit volume. */
  liveSolid(override = {}) {
    const D = this.data;
    const dist = Object.fromEntries(D.forms.map((f) => [f.key, this.live.on[f.key] ? override[f.key] ?? this.live.dist[f.key] : null]));
    const eff = effectiveDistances(D, dist, D.axis ? this.live.t : 0, 1);
    const planes = planesFor(D, eff);
    if (!planes.length) return { faces: [], open: true, planes, s: 1 };
    const B = 4 * Math.max(...planes.map((q) => q.d));
    let faces = solidFrom(planes, B);
    const open = faces.some((f) => f.form === 'box');
    // rescale to unit volume so the view stays comparable while dragging
    const V = volume(faces);
    let s = 1;
    if (!open && V > 0) {
      s = V ** (-1 / 3);
      faces = faces.map((f) => ({ ...f, loop: f.loop.map((q) => mul(q, s)) }));
    }
    return { faces, open, planes, s };
  }

  /** Step 4: the newest form's planes slide in from outside, cutting the solid as they go, then fade. */
  sweepCut() {
    const D = this.data, p = this.cell.params, R = this.R;
    const keys = this.order.slice(0, this.cut).map((f) => f.key);
    const f = this.order[this.cut - 1];
    const d = p.planes[f.key], far = Math.max(1.6 * d, d + 0.7 * R);
    const t0 = performance.now(), T = 1500 * motion(), F = 700 * motion();
    this.anim = (t) => {
      const e = t - t0, dd = far + (d - far) * ease(Math.min(1, e / T));
      if (e > T + F) { this.view.set(this.defs[this.step].scene()); return false; }
      const faces = solidFrom(planesFor(D, { ...p.planes, [f.key]: dd }, keys), 1.5 * R);
      const discs = planeDiscs(f.normals.map((n) => ({ n, d: dd, color: f.color })), 0.75 * R, { opacity: 0.22 });
      fade(discs, e < T ? 1 : 1 - (e - T) / F);
      this.view.set([crystalObject(faces, D, { highlight: f.key }), discs]);
      return true;
    };
  }

  /** Step 3: animate symmetry stages [from, to): each element swings, reflects or inverts the faces made so far. */
  playSym(from, to) {
    const MOVE = 1300 * motion(), HOLD = 650 * motion(), LEAD = (from === 0 && to > 1 ? 900 : 150) * motion();
    const t0 = performance.now();
    this.symBuild(from, 0, from > 0 ? from - 1 : null);
    if (from >= to) { this.symAt = to; return; }
    this.anim = (t) => {
      const e = t - t0 - LEAD;
      if (e < 0) return true;
      const i = from + Math.floor(e / (MOVE + HOLD));
      if (i >= to) {
        this.symAt = to;
        this.symBuild(to, 0, to < this.stages.length ? to - 1 : null);
        return false;
      }
      const s = (e - (i - from) * (MOVE + HOLD)) / MOVE;
      if (s >= 1) this.symBuild(i + 1, 0, i); else this.symBuild(i, ease(s), i);
      return true;
    };
  }

  /** Draw step 3 with `at` stages applied and stage `at` a fraction s under way; `el` is the stage whose element is shown. */
  symBuild(at, s, el) {
    const D = this.data, R = this.R, st = this.stages;
    if (!this.symRoot) return;
    const facesOf = (key, n) => this.final.filter((f) => f.form === key && dot(f.n, n) > 1 - 1e-6);
    const color = Object.fromEntries(this.present.map((f) => [f.key, f.color]));
    const arrow = (n, key) => vectorArrow(mul(n, 1.3 * R), color[key], null, R, { head: 0.07 });
    const key = `${at}|${el}`;
    if (this.symDrawn !== key) {
      this.symDrawn = key;
      for (const c of [...this.symRoot.children]) dispose(c);
      const made = Object.fromEntries(this.present.map((f) => [f.key, [f.normals[0]]]));
      for (const stage of st.slice(0, at)) for (const m of stage.moves) made[m.form].push(m.to);
      const faces = this.present.flatMap((f) => made[f.key].flatMap((n) => facesOf(f.key, n)));
      const stat = new THREE.Group();
      if (faces.length) stat.add(crystalObject(faces, D));
      stat.add(inCrystalFrame(...this.present.flatMap((f) => made[f.key].map((n) => arrow(n, f.key)))));
      if (el != null && st[el]) stat.add(symmetryElement(st[el].op, R));
      this.symStatic = stat;
      this.symDyn = new THREE.Group();
      this.symRoot.add(stat, this.symDyn);
      this.symText(at, el);
    }
    for (const c of [...this.symDyn.children]) dispose(c);
    if (s > 0 && st[at]) {
      const moving = [], arrows = [];
      for (const m of st[at].moves) {
        const P = partialOp(m.M, s);
        for (const f of facesOf(m.form, m.from)) moving.push(movedFace(f, f.loop.map((q) => apply(P, q)), apply(P, f.n)));
        const n = apply(P, m.from);
        if (len(n) > 0.15) arrows.push(arrow(n, m.form));
      }
      if (moving.length) this.symDyn.add(crystalObject(moving, D));
      if (arrows.length) this.symDyn.add(inCrystalFrame(...arrows));
    }
  }

  symText(at, el) {
    const li = document.querySelector('#learn-steps .step.on .body');
    const out = li?.querySelector('[data-symtext]');
    if (!out) return;
    const st = this.stages, total = (i) => this.present.reduce((s, f) => s + (i ? st[i - 1].counts[f.key] : 1), 0);
    const active = el != null ? el + 1 : at;
    li.querySelectorAll('[data-sym]').forEach((b) => b.classList.toggle('on', +b.dataset.sym === active));
    if (el == null) {
      out.innerHTML = at === 0
        ? `Start with one face of each form: ${this.present.map((f) => `<span class="sw" style="background:${f.color}"></span>${esc(paren(f.hkls[0]))}`).join(' ')}.`
        : `All ${st.length} elements applied: <strong>${total(at)}</strong> face planes, every face of every form.`;
      return;
    }
    const { op } = st[el];
    const turns = [...new Set(st[el].moves.map((m) => m.k))].sort((a, b) => a - b).map((k) => `${f3((k * 360) / op.order, 0)}°`).join(', ');
    const what = {
      rotation: () => `<strong>${op.order}-fold rotation axis</strong> along ${esc(axisName(op.axis))}: each face is turned by ${turns}.`,
      mirror: () => `<strong>Mirror plane</strong> perpendicular to ${esc(axisName(op.normal))}: each face is reflected through it.`,
      inversion: () => '<strong>Inversion centre</strong> 1̄: each face (hkl) is sent through the centre to (h̄k̄l̄) on the opposite side.',
      rotoinversion: () => `<strong>${esc(op.symbol)} rotoinversion axis</strong> along ${esc(axisName(op.axis))}: turn by ${f3(360 / parseInt(op.symbol, 10), 0)}°, then invert through the centre.`,
    }[op.kind]();
    const again = st.slice(0, el).some((x) => x.op.symbol === op.symbol && String(x.op.axis) === String(op.axis)) ? ' Applied again, because the faces made since then need their own copies.' : '';
    const counts = this.present.map((f) => `${esc(f.label)} ${el ? st[el - 1].counts[f.key] : 1} → ${st[el].counts[f.key]}`).join(' · ');
    out.innerHTML = `${what}${again}<br><span class="muted">${counts} (total ${total(el)} → ${total(el + 1)})</span>`;
  }

  renderSteps() {
    this.defs = this.steps();
    $('#learn-steps').innerHTML = this.defs.map((s, i) => `<li class="step" data-i="${i}"><h3><span class="num">${i + 1}</span>${esc(s.title)}</h3><div class="body"></div></li>`).join('');
    $('#learn-dots').innerHTML = this.defs.map((_, i) => `<button type="button" data-i="${i}" aria-label="Step ${i + 1}"></button>`).join('');
    document.querySelectorAll('#learn-steps .step').forEach((li) => {
      li.onclick = (e) => { if (+li.dataset.i !== this.step && !e.target.closest('a, button, input, label')) this.go(+li.dataset.i); };
    });
    document.querySelectorAll('#learn-dots button').forEach((b) => { b.onclick = () => this.go(+b.dataset.i); });
  }

  go(i, force = false) {
    if (!this.defs) return;
    i = Math.max(0, Math.min(this.defs.length - 1, i));
    if (i === this.step && !force && this._shown) return;
    const prevStep = this.step;
    this.step = i;
    this._shown = true;
    const def = this.defs[i];
    this.anim = null;
    def.enter?.();
    this.legend(this.present);
    document.querySelectorAll('#learn-steps .step').forEach((li, k) => {
      li.classList.toggle('on', k === i);
      const body = li.querySelector('.body');
      if (k === i) body.innerHTML = def.body(); else body.innerHTML = '';
    });
    document.querySelectorAll('#learn-dots button').forEach((b, k) => b.classList.toggle('on', k === i));
    $('#learn-badge').textContent = `Step ${i + 1} of ${this.defs.length} · ${this.data.name} ${this.cell.label}`;
    $('#learn-prev').disabled = i === 0;
    $('#learn-next').disabled = i === this.defs.length - 1;
    this.view.set(def.scene(), this.R * (def.fitR || 1.15));
    const li = document.querySelector(`#learn-steps .step[data-i="${i}"]`);
    def.bind?.(li.querySelector('.body'), { entered: prevStep !== i || !force });
    const narrow = matchMedia('(max-width: 999px)').matches;
    if (prevStep !== i && (narrow || li.getBoundingClientRect().top < 70)) li.scrollIntoView({ block: 'start', behavior: 'smooth' });
  }

  refresh() {
    if (this.data && !$('#page-learn').hidden) this.go(this.step, true);
  }

  frame() {
    if (this.anim && this.anim(performance.now()) === false) this.anim = null;
    this.view.frame();
  }
}
