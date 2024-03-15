import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(
            0,
            0,
            num_rows,
            num_cols,
            10,
            10,
        )
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_cell_start(self):
        num_cols = 12
        num_rows = 10
        m2 = Maze(
            0,
            0,
            num_rows,
            num_cols,
            10,
            20,
        )
        first_cell = m2._cells[0][0]
        self.assertEqual(first_cell._x1, m2._start.x)
        self.assertEqual(first_cell._y1, m2._start.y)

    def test_maze_broken_start_end(self):
        num_cols = 5
        num_rows = 5
        m = Maze(0, 0, num_rows, num_cols, 5, 5)
        m._break_entrance_and_exit()
        self.assertEqual(m._cells[0][0].has_top_wall, False)
        self.assertEqual(m._cells[-1][-1].has_bottom_wall, False)


if __name__ == "__main__":
    unittest.main()
