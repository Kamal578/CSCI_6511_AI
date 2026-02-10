import unittest
import tempfile
import os

from npuzzle_astar import (
    read_board,
    is_solvable,
    inversion_count,
    goal_board,
    manhattan,
    linear_conflict,
    heuristic,
    neighbors,
    astar,
    build_goal_positions
)


class TestNPuzzleParsing(unittest.TestCase):

    def _write_temp(self, content: str) -> str:
        fd, path = tempfile.mkstemp(text=True)
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path

    def test_tab_delimited_with_blank(self):
        content = "1\t2\t3\n4\t5\t\n7\t8\t6\n"
        path = self._write_temp(content)

        n, board = read_board(path)
        os.remove(path)

        self.assertEqual(n, 3)
        self.assertEqual(board, (1, 2, 3, 4, 5, 0, 7, 8, 6))

    def test_space_aligned_with_zero(self):
        content = "1 2 3\n4 5 6\n7 8 0\n"
        path = self._write_temp(content)

        n, board = read_board(path)
        os.remove(path)

        self.assertEqual(board, (1, 2, 3, 4, 5, 6, 7, 8, 0))


class TestSolvability(unittest.TestCase):

    def test_inversion_count(self):
        self.assertEqual(inversion_count([1, 2, 3, 4, 5, 6, 7, 8, 0]), 0)
        self.assertEqual(inversion_count([1, 2, 3, 4, 5, 6, 8, 7, 0]), 1)

    def test_solvable_3x3(self):
        solvable = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        unsolvable = (1, 2, 3, 4, 5, 6, 8, 7, 0)

        self.assertTrue(is_solvable(3, solvable))
        self.assertFalse(is_solvable(3, unsolvable))


class TestHeuristics(unittest.TestCase):

    def setUp(self):
        self.n = 3
        self.goal = goal_board(self.n)
        self.goal_pos = build_goal_positions(self.n)

    def test_manhattan_goal_is_zero(self):
        self.assertEqual(manhattan(self.n, self.goal, self.goal_pos), 0)

    def test_linear_conflict_goal_is_zero(self):
        self.assertEqual(linear_conflict(self.n, self.goal, self.goal_pos), 0)

    def test_heuristic_positive(self):
        board = (1, 2, 3, 4, 5, 6, 0, 7, 8)
        h = heuristic(self.n, board, self.goal_pos)
        self.assertGreater(h, 0)


class TestNeighbors(unittest.TestCase):

    def test_neighbors_center(self):
        n = 3
        board = (1, 2, 3,
                 4, 0, 5,
                 6, 7, 8)

        moves = dict(neighbors(n, board))
        self.assertEqual(set(moves.values()), {"U", "D", "L", "R"})
        self.assertEqual(len(moves), 4)

    def test_neighbors_corner(self):
        n = 3
        board = (0, 1, 2,
                 3, 4, 5,
                 6, 7, 8)

        moves = list(neighbors(n, board))
        self.assertEqual(len(moves), 2)


class TestAStar(unittest.TestCase):

    def test_already_solved(self):
        n = 3
        start = goal_board(n)
        result = astar(n, start)

        self.assertEqual(result["moves"], 0)
        self.assertEqual(result["path"], [])

    def test_simple_case(self):
        n = 3
        start = (1, 2, 3,
                 4, 5, 6,
                 7, 0, 8)

        result = astar(n, start)

        self.assertEqual(result["moves"], 1)
        self.assertEqual(result["path"], ["R"])

    def test_solution_reaches_goal(self):
        n = 3
        start = (1, 2, 3,
                 4, 0, 6,
                 7, 5, 8)

        result = astar(n, start)
        self.assertEqual(result["boards"][-1], goal_board(n))


if __name__ == "__main__":
    unittest.main()
