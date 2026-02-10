from __future__ import annotations

"""
Goal-state helpers and human-readable board formatting.

Author: Kamal Ahmadov, Omar Imamverdiyev
"""

from .types import Board


def goal_board(n: int) -> Board:
    """Return the canonical goal board: tiles 1..(n^2-1) then 0 in the bottom-right."""
    return tuple(list(range(1, n * n)) + [0])


def format_board(n: int, b: Board) -> str:
    """
    Pretty-print a board with right-aligned numbers and a blank placeholder.

    Keeps uniform width based on the largest tile to preserve grid alignment.
    """
    w = len(str(n * n - 1))
    out_lines = []
    for r in range(n):
        row = b[r * n : (r + 1) * n]
        out_lines.append(" ".join((" " * w if x == 0 else str(x).rjust(w)) for x in row))
    return "\n".join(out_lines)


__all__ = ["goal_board", "format_board"]
