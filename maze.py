from cell import Cell, Point
import time
import random


class Maze:

    def __init__(
        self,
        x1: int,
        y1: int,
        rows: int,
        cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win=None,
        seed=None,
    ) -> None:
        self._cell_x = cell_size_x
        self._cell_y = cell_size_y
        self._start = Point(x1, y1)
        self._nrows = rows
        self._ncols = cols
        self._win = win
        self._create_cells()
        if seed is not None:
            self._seed = random.seed(seed)
        self._animated_once = False

    def _create_cells(self):
        self._cells = [[] for _ in range(self._ncols)]
        for i, lst in enumerate(self._cells):
            curr_x_min = self._start.x + i * self._cell_x
            for j in range(self._nrows):
                curr_y_min = self._start.y + j * self._cell_y
                lst.append(
                    Cell(
                        curr_x_min,
                        curr_y_min,
                        curr_x_min + j * self._cell_x,
                        curr_y_min + j * self._cell_y,
                    )
                )

    def _draw_cells(self):
        for i, lst in enumerate(self._cells):
            curr_x_min = self._start.x + i * self._cell_x
            for j, cell in enumerate(lst):
                curr_y_min = self._start.y + j * self._cell_y
                cell.set_xmin(curr_x_min)
                cell.set_ymin(curr_y_min)
                cell.change_size(self._cell_x, self._cell_y)
        self._animate()

    # https://excalidraw.com/#json=Hey_ibGaXQqoKmQL65aGL,EUAku5zGkgZD7gd-ZIMv9A
    def _animate(self):
        if not self._animated_once:
            sleeptime = 0.05
        else:
            sleeptime = 0.0001
        for i in self._cells:
            for j in i:
                j.draw(self._win.get_canvas(), "black")
                self._win.redraw()
                time.sleep(sleeptime)
        self._break_entrance_and_exit()
        first_cell = self._cells[0][0]
        last_cell = self._cells[-1][-1]
        first_cell.draw(self._win.get_canvas(), "black")
        last_cell.draw(self._win.get_canvas(), "black")
        self._animated_once = True

    def _break_entrance_and_exit(self):
        """
        Entrance to maze always top of top left cell (First cell)
        Exit will always be bottom of bottom left (last cell)
        this function removes the Cell walls for those
        """
        first_cell = self._cells[0][0]
        last_cell = self._cells[-1][-1]
        first_cell.has_top_wall = False
        last_cell.has_bottom_wall = False

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_directions = []
            # i is cols, j is rows
            # if we are at first col, cannot move left
            # if left visited also cannot move left
            if i > 0 and not self._cells[i - 1][j].visited:
                possible_directions.append((i - 1, j))
            # if we are at the last col, cannot move right
            if i < self._ncols - 1 and not self._cells[i + 1][j].visited:
                possible_directions.append((i + 1, j))
            # if we are at the first row or above is visited, can't go up:
            if j > 0 and not self._cells[i][j - 1].visited:
                possible_directions.append((i, j - 1))
            # can only move down if we are not the last rows
            # and below hasn't been visited
            if j < self._nrows - 1 and not self._cells[i][j + 1].visited:
                possible_directions.append((i, j + 1))
            if len(possible_directions) == 0:
                self._cells[i][j].draw(
                    canvas=self._win.get_canvas(), fill_color="black"
                )
                return
            i_next, j_next = random.choice(possible_directions)
            # todo break walls between cell to move to
            current_cell = self._cells[i][j]
            next_cell = self._cells[i_next][j_next]
            if i_next == i + 1:
                # move right
                current_cell.has_right_wall = False
                next_cell.has_left_wall = False

            # move left
            if i_next == i - 1:
                current_cell.has_left_wall = False
                next_cell.has_right_wall = False
            # move up
            if j_next == j - 1:
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            # move down
            if j_next == j + 1:
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False

            self._break_walls_r(i_next, j_next)
            possible_directions.remove((i_next, j_next))

    def _reset_cells_visited(self):
        for i in self._cells:
            for j in i:
                j.visited = False

    def _solve(self):
        solved = self._solve_r(0, 0)
        return solved

    def _solve_r(self, i, j):
        winner_cell = self._cells[self._ncols - 1][self._nrows - 1]
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if current_cell is winner_cell:
            return True
        # check left
        if (
            i > 0
            and not current_cell.has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            current_cell.draw_move(self._win.get_canvas(), self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                current_cell.draw_move(
                    self._win.get_canvas(), self._cells[i - 1][j], undo=True
                )

        # check right
        if (
            i < self._ncols - 1
            and not current_cell.has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            current_cell.draw_move(self._win.get_canvas(), self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                current_cell.draw_move(
                    self._win.get_canvas(), self._cells[i + 1][j], undo=True
                )
        # check up
        if (
            j > 0
            and not current_cell.has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            current_cell.draw_move(self._win.get_canvas(), self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                current_cell.draw_move(
                    self._win.get_canvas(), self._cells[i][j - 1], undo=True
                )
        # check down
        if (
            j < self._nrows - 1
            and not current_cell.has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            current_cell.draw_move(self._win.get_canvas(), self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                current_cell.draw_move(
                    self._win.get_canvas(), self._cells[i][j + 1], undo=True
                )
        return False
