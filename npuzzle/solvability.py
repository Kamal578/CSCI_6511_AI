from __future__ import annotations

"""
Solvability checks for the n-puzzle.

Rules:
- Odd n: puzzle solvable iff inversion count is even.
- Even n: solvable iff (blank row from bottom is even AND inversions odd)
          OR (blank row from bottom is odd AND inversions even).

Author: Kamal Ahmadov, Omar Imamverdiyev
"""

from .types import Board


def inversion_count(seq: Board) -> int:
    """Count inversions in the board (ignoring the blank) using O(k^2) scan."""
    arr = [x for x in seq if x != 0]
    inv = 0
    for i in range(len(arr)):
        ai = arr[i]
        for j in range(i + 1, len(arr)):
            if ai > arr[j]:
                inv += 1
    return inv


def is_solvable(n: int, b: Board) -> bool:
    """Return True iff the board configuration is solvable for given n."""
    inv = inversion_count(list(b))
    if n % 2 == 1:
        # odd grid: solvable if inversions even
        return inv % 2 == 0

    # even grid:
    # row of blank counted from bottom starting at 1
    blank_idx = b.index(0)
    blank_row_from_top = blank_idx // n  # 0-based
    blank_row_from_bottom = n - blank_row_from_top  # 1..n
    # solvable iff:
    #   blank on even row from bottom and inversions odd
    #   OR blank on odd row from bottom and inversions even
    if blank_row_from_bottom % 2 == 0:
        return inv % 2 == 1
    else:
        return inv % 2 == 0


__all__ = ["inversion_count", "is_solvable"]
