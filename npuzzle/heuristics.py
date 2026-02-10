from __future__ import annotations

"""
Admissible heuristic components for the n-puzzle.

The solver uses Manhattan distance plus Linear Conflict. The sum remains
admissible and consistent, giving optimality while pruning more nodes than
Manhattan alone.
"""

from typing import List, Tuple

from .types import Board


def build_goal_positions(n: int) -> List[Tuple[int, int]]:
    """
    Precompute goal coordinates for every tile value (0..n^2-1).

    Returns a list where index = tile value, value = (row, col) in goal state.
    """
    pos = [(0, 0)] * (n * n)
    # 1..N
    for val in range(1, n * n):
        idx = val - 1
        pos[val] = (idx // n, idx % n)
    # 0 at the end
    pos[0] = (n - 1, n - 1)
    return pos


def manhattan(n: int, b: Board, goal_pos: List[Tuple[int, int]]) -> int:
    """
    Sum of vertical + horizontal distances from each tile to its goal spot.

    Ignores the blank (0). Standard admissible heuristic for sliding puzzles.
    """
    dist = 0
    for idx, val in enumerate(b):
        if val == 0:
            continue
        r, c = divmod(idx, n)
        gr, gc = goal_pos[val]
        dist += abs(r - gr) + abs(c - gc)
    return dist


def linear_conflict(n: int, b: Board, goal_pos: List[Tuple[int, int]]) -> int:
    """
    Extra cost for tiles in the correct row/col but reversed order (adds 2 per pair).

    Counts inversions among goal-aligned tiles in each row/column. Adds 2 moves per
    conflict, preserving admissibility when combined with Manhattan.
    """
    conflict = 0

    # Row conflicts
    for r in range(n):
        row_tiles: List[int] = []
        for c in range(n):
            val = b[r * n + c]
            if val != 0 and goal_pos[val][0] == r:
                row_tiles.append(val)
        # count inversions by goal column among these tiles
        for i in range(len(row_tiles)):
            gi = goal_pos[row_tiles[i]][1]
            for j in range(i + 1, len(row_tiles)):
                gj = goal_pos[row_tiles[j]][1]
                if gi > gj:
                    conflict += 2

    # Column conflicts
    for c in range(n):
        col_tiles: List[int] = []
        for r in range(n):
            val = b[r * n + c]
            if val != 0 and goal_pos[val][1] == c:
                col_tiles.append(val)
        # count inversions by goal row among these tiles
        for i in range(len(col_tiles)):
            gi = goal_pos[col_tiles[i]][0]
            for j in range(i + 1, len(col_tiles)):
                gj = goal_pos[col_tiles[j]][0]
                if gi > gj:
                    conflict += 2

    return conflict


def heuristic(n: int, b: Board, goal_pos: List[Tuple[int, int]]) -> int:
    """Admissible combined heuristic = Manhattan + Linear Conflict."""
    return manhattan(n, b, goal_pos) + linear_conflict(n, b, goal_pos)


__all__ = [
    "build_goal_positions",
    "manhattan",
    "linear_conflict",
    "heuristic",
]
