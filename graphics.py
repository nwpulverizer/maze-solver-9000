from tkinter import Tk, Canvas


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root)
        self.__canvas.pack()
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def get_canvas(self):
        return self.__canvas

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()

    def close(self):
        self.__is_running = False

    def draw_line(self, line, fill_color: str):
        line.draw(self.__canvas, fill_color)

    def draw_cell(self, cell, fill_color):
        cell.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


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

    def draw(self, canvas: Canvas, fill_color: str) -> None:
        if self.has_left_wall:
            wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            wall.draw(canvas, fill_color)
        if self.has_right_wall:
            wall = Line(Point(self._x2, self._y2), Point(self._x2, self._y1))
            wall.draw(canvas, fill_color)
        # again, canvas top left is x1 y1
        if self.has_bottom_wall:
            wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            wall.draw(canvas, fill_color)
        if self.has_top_wall:
            wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            wall.draw(canvas, fill_color)

    def draw_move(self, canvas, to_cell, undo=False):
        line = Line(self._center, to_cell._center)
        if undo:
            line.draw(canvas, fill_color="gray")
        else:
            line.draw(canvas, fill_color="red")
