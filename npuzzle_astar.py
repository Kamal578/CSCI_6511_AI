"""
A* solver for the N-Puzzle.

This file now serves as a thin CLI wrapper. Core logic lives in the
`npuzzle` package, which separates parsing, heuristics, solvability checks,
search, and command-line handling into focused modules.

Author: Kamal Ahmadov, Omar Imamverdiyev
"""

from npuzzle.cli import main

if __name__ == "__main__":
    main()
