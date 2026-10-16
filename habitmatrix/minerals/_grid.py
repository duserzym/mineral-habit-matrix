"""Declarative habit matrices.

A matrix is a list of row levels and a list of column levels.  Each level carries a short
code, a header label/detail and a list of *operations*; a cell applies the row's and then
the column's operations to the base distances.  Operations:

    {"pair": [keep, vary, frac], "mode": "prism"|"area"}   relative development of two forms
    {"share": [key, share, ref], "among": [...]}           area share of one form
    {"set": {key: d or None}}                              absolute central distance (None = absent)
    {"scale": {key: factor}}                               multiply a distance
    {"rel": {key: [ref, factor]}}                          d[key] = factor * d[ref] (absent if ref is)
    {"fn": callable}                                       d -> new d, for anything else
    any op may carry "requires": key — it is skipped when that form is absent
    {"aspect": value}                                      length/width along the measure axis

Operations run in stage order (default 0; "rel" and "fn" 0.5; "aspect" 1), so habit ratios
are fixed before the crystal is elongated or flattened; give "stage": 2 to re-balance a form
after the aspect is set.
"""

from __future__ import annotations

from ..habit import ABSENT, Crystal, Form, solve_aspect, solve_pair, solve_share
from ..lattice import Lattice


def form(key, index, name, color):
    return Form(key, tuple(index), name, color)


def _apply(crystal: Crystal, d: dict, t: float, op: dict):
    if op.get("requires") and d.get(op["requires"]) is None:
        return d, t  # optional op: skipped when the form it depends on is absent
    if "set" in op:
        d = {**d, **op["set"]}
    elif "scale" in op:
        d = {**d, **{k: d[k] * f for k, f in op["scale"].items()}}
    elif "pair" in op:
        keep, vary, frac = op["pair"]
        mode = op.get("mode", "area")
        d = solve_pair(crystal, d, keep, vary, frac, mode=mode, t=op.get("t", 50.0 if crystal.axis is not None else 0.0))
    elif "share" in op:
        key, share, ref = op["share"]
        if share > 0 and d.get(key) is None:
            d = {**d, key: d[ref]}
        d = solve_share(crystal, d, key, share, ref, among=op.get("among"), t=op.get("t", t))
    elif "rel" in op:
        d = dict(d)
        for k, (r, f) in op["rel"].items():
            d[k] = None if d.get(r) is None else f * d[r]
    elif "fn" in op:
        d = op["fn"](dict(d))
    elif "aspect" in op:
        t = solve_aspect(crystal, d, op["aspect"])
    else:
        raise ValueError(f"unknown op {op}")
    return d, t


def build_cell(crystal: Crystal, base: dict, ops: list[dict]):
    def stage(op):
        return op.get("stage", 1 if "aspect" in op else 0.5 if ("rel" in op or "fn" in op) else 0)

    staged = sorted(enumerate(ops), key=lambda io: (stage(io[1]), io[0]))
    d, t = dict(base), 0.0
    for _, op in staged:
        d, t = _apply(crystal, d, t, op)
    return d, t


def grid_spec(*, id, name, formula, group, chronometers, system, setting, lattice, lattice_source,
              point_group, forms, base, rows, cols, title, subtitle, row_title, col_title, note="",
              about="", habits=(), references=(), elongation_axis=(0, 0, 1), measure_plane=None,
              mono_color="#9aa0a6", view=None, default=None, skip=()):
    """Return the spec dict consumed by habitmatrix.build."""
    crystal = Crystal(id, Lattice(**lattice), point_group, list(forms),
                      elongation_axis=elongation_axis, measure_plane=measure_plane)
    cells = []
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            if (i, j) in skip:
                continue
            try:
                d, t = build_cell(crystal, {k: base.get(k, ABSENT) for k in [f.key for f in forms]},
                                  list(r.get("ops", [])) + list(c.get("ops", [])))
            except Exception as e:  # make failures easy to locate
                raise RuntimeError(f"{id} cell row {i} ({r['code']}) col {j} ({c['code']}): {e}") from e
            code = f"{r['code']}{c['code']}"
            cells.append({
                "id": code, "row": i, "col": j, "label": code, "sub": "",
                "title": f"{code}: {r.get('text', r['label'])} · {c.get('text', c['label'])}",
                "description": f"{r.get('text', r['label'])}; {c.get('text', c['label'])}.",
                "default": (i, j) == (default or (len(rows) // 2, len(cols) // 2)),
                "distances": d, "t": t,
            })
    return {
        "id": id, "name": name, "crystal": crystal, "formula": formula, "group": group,
        "chronometers": chronometers, "system": system, "setting": setting,
        "lattice_source": lattice_source, "mono_color": mono_color, "view": view or {},
        "matrix": {
            "title": title, "subtitle": subtitle, "row_title": row_title, "col_title": col_title,
            "rows": [{"label": r["label"], "detail": r.get("detail", "")} for r in rows],
            "cols": [{"label": c["label"], "detail": c.get("detail", "")} for c in cols],
            "note": note,
        },
        "about": about, "habits": list(habits), "references": list(references), "cells": cells,
    }
