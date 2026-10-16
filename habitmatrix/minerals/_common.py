"""Shared helpers for building habit matrices."""

from __future__ import annotations

from ..habit import ABSENT, Crystal, solve_aspect, solve_pair


def ref(citation: str, doi: str | None = None, note: str = "", tags=(), url: str | None = None) -> dict:
    return {"citation": citation, "doi": doi, "url": url, "note": note, "tags": list(tags)}


def prism_then_cap(crystal: Crystal, base: dict, prism: tuple | None, cap: tuple | None, aspect: float | None,
                   cap_t: float = 50.0):
    """Distances for a prismatic habit.

    prism = (keep, vary, fraction_of_keep_in_cross_section)
    cap   = (keep, vary, fraction_of_keep_in_termination_area)
    aspect: target length/width along the elongation axis (None = leave caps as they are).
    cap_t: cap translation at which termination areas are measured (use 0 for habits
           without a prism, e.g. a pure dipyramid, where the caps meet).
    """
    d = dict(base)
    if prism is not None:
        k, v, f = prism
        d = solve_pair(crystal, d, k, v, f, mode="prism")
    if cap is not None:
        k, v, f = cap
        d = solve_pair(crystal, d, k, v, f, mode="area", t=cap_t)
    t = solve_aspect(crystal, d, aspect) if aspect else 0.0
    return d, t


def frac_text(a: str, b: str, f: float) -> str:
    """Human-readable relative development, e.g. '{100} ≈ {110}'."""
    if f >= 0.999:
        return f"{a} only"
    if f <= 0.001:
        return f"{b} only"
    if abs(f - 0.5) < 0.02:
        return f"{a} = {b}"
    return f"{a} {'>' if f > 0.5 else '<'} {b}"


__all__ = ["ABSENT", "ref", "prism_then_cap", "frac_text"]
