// Step-by-step reconstruction of any crystal in the matrix, from lattice to exported solid.
import { SoloView, crystalObject, cellFrame, vectorArrow, viewQ, inCrystalFrame } from './views.js';
import {
  planesFor, solidFrom, formAreas, effectiveDistances, volume, aspect, radius, dot, len, angle, fmtIndex, mul,
} from './geom.js';

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const f3 = (x, d = 3) => Number(x).toFixed(d);
const vec = (v, d = 3) => `(${v.map((x) => f3(x, d)).join(', ')})`;
const paren = (idx) => `(${fmtIndex(idx)})`;
const AXIS_COLORS = ['#e5484d', '#30a46c', '#0090ff'];

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
          const objs = [];
          for (const f of this.present) for (const n of f.normals) objs.push(vectorArrow(mul(n, 1.3 * R), f.color, null, R, { head: 0.07 }));
          return [ghost(), inCrystalFrame(...objs)];
        },
        body: () => {
          const rows = this.present.map((f) => `<tr><td><span class="sw" style="background:${f.color};display:inline-block;vertical-align:-1px"></span> ${esc(f.label)}</td><td class="num">${f.normals.length}</td><td class="num">${f.hkls.slice(0, 6).map((h) => esc(paren(h))).join(' ')}${f.hkls.length > 6 ? ' …' : ''}</td></tr>`).join('');
          return `
          <p>The point group <strong>${esc(D.point_group)}</strong> has ${D.pg_order} symmetry operations. Applying all of them to one face
          generates the whole <em>form</em> {hkl}, the set of faces that are equivalent by symmetry. Every face of a form sits at the
          <strong>same distance</strong> from the centre, which is why real crystals look symmetric.</p>
          <table><tr><th>form</th><th>faces</th><th>indices</th></tr>${rows}</table>
          <p>The arrows show every face normal present in this crystal: ${this.present.reduce((s, f) => s + f.normals.length, 0)} planes in total.</p>`;
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
          <p class="muted">A plane that misses the solid simply leaves no face. That is how forms appear and disappear across a typology grid.</p>`;
        },
        bind: (el) => {
          el.querySelectorAll('[data-cut]').forEach((b) => {
            b.onclick = (e) => { e.stopPropagation(); this.cut = +b.dataset.cut; this.go(this.step, true); };
          });
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
          const refresh = () => {
            const { faces, open } = this.liveSolid();
            this.view.set(crystalObject(faces, D), Math.max(radius(faces), 1e-3) * 1.3);
            const areas = formAreas(faces);
            const tot = Object.values(areas).reduce((a, b) => a + b, 0);
            el.querySelector('[data-bar]').innerHTML = D.forms.filter((f) => areas[f.key]).map((f) => `<span style="width:${(100 * areas[f.key]) / tot}%;background:${f.color}"></span>`).join('');
            el.querySelector('[data-stats]').innerHTML = open
              ? 'The solid is open: switch on a termination form or move faces inward.'
              : `${faces.length} faces · ${D.forms.filter((f) => areas[f.key]).map((f) => `${esc(f.label)} ${f3((100 * areas[f.key]) / tot, 0)}%`).join(' · ')} · aspect ${f3(aspect(faces, D.measure_axis || u), 2)}`;
            this.legend(D.forms.filter((f) => areas[f.key]));
          };
          el.querySelectorAll('[data-d]').forEach((s) => {
            s.oninput = () => {
              const k = s.dataset.d;
              this.live.dist[k] = this.refDist() * 10 ** +s.value;
              el.querySelector(`[data-o="${k}"]`).textContent = f3(this.live.dist[k], 3);
              refresh();
            };
          });
          el.querySelectorAll('[data-on]').forEach((c) => {
            c.onchange = () => {
              const k = c.dataset.on;
              this.live.on[k] = c.checked;
              if (c.checked && this.live.dist[k] == null) this.live.dist[k] = this.defaultDist(k);
              el.querySelector(`[data-d="${k}"]`).disabled = !c.checked;
              refresh();
            };
          });
          const ts = el.querySelector('[data-t]');
          if (ts) ts.oninput = () => { this.live.t = +ts.value; el.querySelector('[data-o="t"]').textContent = f3(this.live.t, 2); refresh(); };
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

  liveSolid() {
    const D = this.data;
    const dist = Object.fromEntries(D.forms.map((f) => [f.key, this.live.on[f.key] ? this.live.dist[f.key] : null]));
    const eff = effectiveDistances(D, dist, D.axis ? this.live.t : 0, 1);
    const planes = planesFor(D, eff);
    if (!planes.length) return { faces: [], open: true };
    const B = 4 * Math.max(...planes.map((q) => q.d));
    let faces = solidFrom(planes, B);
    const open = faces.some((f) => f.form === 'box');
    // rescale to unit volume so the view stays comparable while dragging
    const V = volume(faces);
    if (!open && V > 0) {
      const s = V ** (-1 / 3);
      faces = faces.map((f) => ({ ...f, loop: f.loop.map((q) => mul(q, s)) }));
    }
    return { faces, open };
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
    def.bind?.(li.querySelector('.body'));
    if (prevStep !== i && li.getBoundingClientRect().top < 70) li.scrollIntoView({ block: 'start', behavior: 'smooth' });
  }

  refresh() {
    if (this.data && !$('#page-learn').hidden) this.go(this.step, true);
  }

  frame() {
    this.view.frame();
  }
}
