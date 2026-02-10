from __future__ import annotations

import re
from typing import List, Tuple

from .types import Board


def read_board(path: str) -> Tuple[int, Board]:
    with open(path, "r", encoding="utf-8") as f:
        raw_lines = [ln.rstrip("\n") for ln in f if ln.strip() != ""]

    n = len(raw_lines)
    if not (3 <= n <= 8):
        raise ValueError(f"n must be between 3 and 8, got n={n}")

    # ---------- Case 1: TAB-delimited (preserve empty cells) ----------
    # If there are tabs, parse by '\t' so empty tokens survive.
    if any("\t" in ln for ln in raw_lines):
        rows: List[List[int]] = []
        for ln in raw_lines:
            parts = ln.split("\t")
            # If teacher used tabs, we expect exactly n columns.
            # If not, we'll fall back to space-aligned parsing below.
            if len(parts) != n:
                rows = []
                break
            row: List[int] = []
            for cell in parts:
                cell = cell.strip()
                row.append(0 if cell == "" else int(cell))
            rows.append(row)

        if rows:
            flat = [x for r in rows for x in r]
            expected = set(range(n * n))
            if set(flat) != expected:
                raise ValueError(f"Board must contain all numbers 0..{n*n-1} exactly once.")
            return n, tuple(flat)

    # ---------- Case 2: SPACE-ALIGNED / FIXED-COLUMN parsing ----------
    # Extract numbers with their character start positions.
    # If one row is missing the blank, it will have n-1 numbers.
    num_pat = re.compile(r"\d+")
    row_matches = []
    counts = []

    for ln in raw_lines:
        matches = [(m.group(0), m.start()) for m in num_pat.finditer(ln)]
        row_matches.append(matches)
        counts.append(len(matches))

    max_count = max(counts)
    # If all rows already have n numbers, just parse them normally.
    if max_count == n and all(c == n for c in counts):
        rows = [[int(tok) for tok, _ in matches] for matches in row_matches]
        flat = [x for r in rows for x in r]
        expected = set(range(n * n))
        if set(flat) != expected:
            raise ValueError(f"Board must contain all numbers 0..{n*n-1} exactly once.")
        return n, tuple(flat)

    # Otherwise, we expect exactly one row to have n-1 numbers (the blank row),
    # and the rest to have n numbers.
    if max_count != n or not all(c in (n, n - 1) for c in counts) or counts.count(n - 1) != 1:
        # Last fallback: plain whitespace split (requires explicit 0)
        rows_ws: List[List[int]] = []
        for ln in raw_lines:
            parts = ln.split()
            rows_ws.append([int(x) for x in parts])
        if any(len(r) != n for r in rows_ws):
            raise ValueError(
                "Could not parse as tab-delimited or space-aligned grid. "
                "If using spaces, the file must be column-aligned; otherwise include 0 for blank."
            )
        flat = [x for r in rows_ws for x in r]
        expected = set(range(n * n))
        if set(flat) != expected:
            raise ValueError(f"Board must contain all numbers 0..{n*n-1} exactly once.")
        return n, tuple(flat)

    # Choose an "anchor" row that has n numbers to infer column start positions.
    anchor_idx = counts.index(n)
    anchors = [pos for _, pos in row_matches[anchor_idx]]

    # Tolerance for aligning numbers to anchors
    diffs = [anchors[i + 1] - anchors[i] for i in range(n - 1)]
    min_step = min(diffs) if diffs else 2
    tol = max(1, min_step // 2)

    def fill_row(matches: List[Tuple[str, int]]) -> List[int]:
        # If already complete, take tokens in order
        if len(matches) == n:
            return [int(tok) for tok, _ in matches]

        # If missing one cell, insert 0 at the missing anchor position.
        out: List[int] = []
        j = 0  # index into matches
        for i in range(n):  # for each anchor/column
            if j >= len(matches):
                out.append(0)
                continue
            tok, pos = matches[j]
            if abs(pos - anchors[i]) <= tol:
                out.append(int(tok))
                j += 1
            else:
                out.append(0)
        if len(out) != n:
            raise ValueError("Internal parse error while reconstructing missing blank.")
        return out

    rows = [fill_row(m) for m in row_matches]
    flat = [x for r in rows for x in r]

    expected = set(range(n * n))
    if set(flat) != expected:
        # Helpful diagnostic
        missing = sorted(expected - set(flat))
        extra = sorted(set(flat) - expected)
        raise ValueError(
            f"Parsed grid, but numbers are wrong. Missing={missing}, Extra={extra}. "
            "Your file may not be consistently column-aligned."
        )

    return n, tuple(flat)


__all__ = ["read_board"]
