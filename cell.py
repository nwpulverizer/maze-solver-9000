from graphics import Line, Point
from tkinter import Canvas


class Cell:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        # x1, y1 is top left, x2,y2 is bottom rigt
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._center = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)
        self.visited = False
        self.animated_once = False

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        if self.has_left_wall:
            wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            wall.draw(canvas, fill_color)
        if not self.has_left_wall:
            wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            wall.draw(canvas, "#d9d9d9")
        if self.has_right_wall:
            wall = Line(Point(self._x2, self._y2), Point(self._x2, self._y1))
            wall.draw(canvas, fill_color)
        if not self.has_right_wall:
            wall = Line(Point(self._x2, self._y2), Point(self._x2, self._y1))
            wall.draw(canvas, "#d9d9d9")
        if self.has_bottom_wall:
            wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            wall.draw(canvas, fill_color)
        if not self.has_bottom_wall:
            wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            wall.draw(canvas, "#d9d9d9")
        if self.has_top_wall:
            wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            wall.draw(canvas, fill_color)
        if not self.has_top_wall:
            wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            wall.draw(canvas, "#d9d9d9")

    def draw_move(self, canvas, to_cell, undo=False):
        # our current position is the _center
        # of our self. Move to center of to_cell by moving up
        # down left and right.
        current_pos = self._center
        fill_color = "red"
        if undo:
            fill_color = "grey"
        if current_pos.x != to_cell._center.x:
            newpos = Point(to_cell._center.x, current_pos.y)
            move = Line(current_pos, newpos)
            move.draw(canvas, fill_color)
            current_pos = newpos
        if current_pos.y != to_cell._center.y:
            newpos = Point(current_pos.x, to_cell._center.y)
            move = Line(current_pos, newpos)
            move.draw(canvas, fill_color)

    def __reset_center(self):
        self._center = Point((self._x1 + self._x2) // 2, (self._y1 + self._y2) // 2)

    def set_xmin(self, xmin):
        self._x1 = xmin
        self.__reset_center()

    def set_ymin(self, ymin):
        self._y1 = ymin
        self.__reset_center()

    def change_size(self, sizex, sizey):
        self._x2 = self._x1 + sizex
        self._y2 = self._y1 + sizey
        self.__reset_center()
