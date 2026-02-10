from __future__ import annotations

from .types import Board


def goal_board(n: int) -> Board:
    # 1..N then 0
    return tuple(list(range(1, n * n)) + [0])


def format_board(n: int, b: Board) -> str:
    w = len(str(n * n - 1))
    out_lines = []
    for r in range(n):
        row = b[r * n : (r + 1) * n]
        out_lines.append(" ".join((" " * w if x == 0 else str(x).rjust(w)) for x in row))
    return "\n".join(out_lines)


__all__ = ["goal_board", "format_board"]
