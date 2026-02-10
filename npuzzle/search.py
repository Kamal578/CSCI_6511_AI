from __future__ import annotations

import heapq
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

from .types import Board, Move
from .heuristics import build_goal_positions, heuristic
from .state import goal_board


def neighbors(n: int, b: Board) -> Iterable[Tuple[Board, Move]]:
    z = b.index(0)
    zr, zc = divmod(z, n)

    def swap_and_yield(nidx: int, mv: Move):
        bb = list(b)
        bb[z], bb[nidx] = bb[nidx], bb[z]
        return (tuple(bb), mv)

    # Moves: U means blank moves up (tile moves down into blank),
    # but move naming is conventional; we’ll use direction of blank movement.
    if zr > 0:
        yield swap_and_yield(z - n, "U")
    if zr < n - 1:
        yield swap_and_yield(z + n, "D")
    if zc > 0:
        yield swap_and_yield(z - 1, "L")
    if zc < n - 1:
        yield swap_and_yield(z + 1, "R")


@dataclass(order=True)
class PQItem:
    f: int
    h: int
    g: int
    board: Board


def astar(n: int, start: Board, use_heuristic: bool = True):
    goal = goal_board(n)
    if start == goal:
        return {
            "moves": 0,
            "path": [],
            "boards": [start],
            "expanded": 0,
            "max_frontier": 0,
            "time": 0.0,
        }

    goal_pos = build_goal_positions(n)

    # For path reconstruction
    parent: Dict[Board, Tuple[Optional[Board], Optional[Move]]] = {start: (None, None)}
    g_best: Dict[Board, int] = {start: 0}

    expanded = 0
    max_frontier = 0
    start_time = time.time()

    h0 = heuristic(n, start, goal_pos) if use_heuristic else 0

    pq: List[PQItem] = []
    heapq.heappush(pq, PQItem(f=h0, h=h0, g=0, board=start))

    while pq:
        cur = heapq.heappop(pq)
        b = cur.board

        # Skip stale PQ entries
        if cur.g != g_best.get(b, 10**18):
            continue

        expanded += 1
        max_frontier = max(max_frontier, len(pq))

        if b == goal:
            elapsed = time.time() - start_time
            # reconstruct
            moves: List[Move] = []
            boards: List[Board] = []
            node: Optional[Board] = b
            while node is not None:
                boards.append(node)
                p, mv = parent[node]
                if mv is not None:
                    moves.append(mv)
                node = p
            boards.reverse()
            moves.reverse()

            return {
                "moves": cur.g,
                "path": moves,
                "boards": boards,
                "expanded": expanded,
                "max_frontier": max_frontier,
                "time": elapsed,
            }

        for nb, mv in neighbors(n, b):
            ng = cur.g + 1
            old = g_best.get(nb)
            if old is None or ng < old:
                g_best[nb] = ng
                parent[nb] = (b, mv)
                nh = heuristic(n, nb, goal_pos) if use_heuristic else 0
                heapq.heappush(pq, PQItem(f=ng + nh, h=nh, g=ng, board=nb))

    raise RuntimeError("No solution found (this should not happen if solvable).")


__all__ = ["neighbors", "PQItem", "astar"]
