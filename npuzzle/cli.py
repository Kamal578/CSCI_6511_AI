from __future__ import annotations

import argparse

from .parsing import read_board
from .solvability import is_solvable
from .search import astar
from .state import format_board


def run_solver(file_path: str, show: bool = False, evaluation: bool = False) -> None:
    n, start = read_board(file_path)

    print(f"n = {n}")
    print("Start:")
    print(format_board(n, start))
    print()

    if not is_solvable(n, start):
        print("This puzzle configuration is NOT solvable.")
        return

    if evaluation:
        print("Running Uniform Cost Search (h = 0)...")
        ucs = astar(n, start, use_heuristic=False)

        print("Running A* with heuristic...")
        astar_h = astar(n, start, use_heuristic=True)

        print("\n=== Evaluation Results ===")
        print("UCS (no heuristic):")
        print(f"  Expanded states: {ucs['expanded']}")
        print(f"  Max frontier size: {ucs['max_frontier']}")
        print(f"  Runtime: {ucs['time']:.3f} seconds")

        print("\nA* with heuristic:")
        print(f"  Expanded states: {astar_h['expanded']}")
        print(f"  Max frontier size: {astar_h['max_frontier']}")
        print(f"  Runtime: {astar_h['time']:.3f} seconds")

        print("\n=== Solution (A* with heuristic) ===")
        print(f"Minimum moves: {astar_h['moves']}")
        print("Move sequence:", "".join(astar_h["path"]))

        if show:
            for i, b in enumerate(astar_h["boards"]):
                print(f"\nStep {i}:")
                print(format_board(n, b))

    else:
        # NORMAL MODE: A* only
        result = astar(n, start, use_heuristic=True)

        print(f"Minimum moves: {result['moves']}")
        print("Move sequence:", "".join(result["path"]))

        if show:
            for i, b in enumerate(result["boards"]):
                print(f"\nStep {i}:")
                print(format_board(n, b))


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Solve n-puzzle using A* (Manhattan + Linear Conflict).")
    ap.add_argument("file", help="Path to input file")
    ap.add_argument("--show", action="store_true", help="Print boards along the solution path.")
    ap.add_argument("--evaluation", action="store_true", help="Compare UCS (h=0) with A* heuristic")
    return ap


def main(argv: list[str] | None = None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    run_solver(args.file, show=args.show, evaluation=args.evaluation)


__all__ = ["build_arg_parser", "main", "run_solver"]
