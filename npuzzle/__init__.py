"""
API for the n-puzzle solver package.

Re-export the main building blocks so callers can simply
`from npuzzle import astar, read_board, heuristic, ...`.

Author: Kamal Ahmadov, Omar Imamverdiyev
"""

from .types import Move, Board
from .parsing import read_board
from .solvability import inversion_count, is_solvable
from .state import goal_board, format_board
from .heuristics import build_goal_positions, manhattan, linear_conflict, heuristic
from .search import neighbors, astar

__all__ = [
    "Move",
    "Board",
    "read_board",
    "inversion_count",
    "is_solvable",
    "goal_board",
    "format_board",
    "build_goal_positions",
    "manhattan",
    "linear_conflict",
    "heuristic",
    "neighbors",
    "astar",
]
