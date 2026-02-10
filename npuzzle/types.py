"""
Shared lightweight type aliases used across the n-puzzle solver.

- `Move` uses the conventional blank movement letters: U, D, L, R.
- `Board` is a flattened n*n tuple in row-major order with `0` representing the blank.
  Using tuples keeps states hashable for fast membership checks in sets/dicts.
"""

from typing import Tuple

Move = str
Board = Tuple[int, ...]

__all__ = ["Move", "Board"]
