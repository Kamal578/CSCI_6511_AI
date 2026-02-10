from __future__ import annotations

from typing import List, Tuple

from .types import Board
from .state import goal_board


def build_goal_positions(n: int) -> List[Tuple[int, int]]:
    """
    goal_pos[val] = (row, col) for val in 0..n*n-1
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
    Linear conflict heuristic component:
    Adds 2 moves for each pair of tiles in the same row/col whose goal positions
    are in that row/col but reversed relative order.

    Total heuristic = Manhattan + linear_conflict
    (still admissible)
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
    return manhattan(n, b, goal_pos) + linear_conflict(n, b, goal_pos)


__all__ = [
    "build_goal_positions",
    "manhattan",
    "linear_conflict",
    "heuristic",
]
