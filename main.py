from cell import Cell
from maze import Maze
from graphics import Line, Point, Window

size = 20
gap = 5
all_walls = Cell(2, 3, size, size)
next_start = size + gap
no_bot = Cell(next_start, next_start, next_start + size, next_start + size)
no_bot.has_bottom_wall = False
next_start += size + gap
no_top = Cell(next_start, next_start, next_start + size, next_start + size)
no_top.has_top_wall = False
next_start += size + gap
no_right = Cell(next_start, next_start, next_start + size, next_start + size)
no_right.has_right_wall = False
no_right.has_right_wall = False


def main():
    win = Window(800, 800)
    maze = Maze(1, 1, 5, 5, 20, 20, win, 0)
    maze._draw_cells()
    maze._break_walls_r(0, 0)
    win.wait_for_close()


main()
