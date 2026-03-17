import math

from kivy.metrics import dp
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.graphics import Line, Color, Rectangle, Point
from kivy.clock import Clock
from gestures4kivy import CommonGestures
from board.board import *
from rect import Rect


class BoardWidget(CommonGestures, MDRelativeLayout):
    # board = Board([
    #     ['x', '-', '-', '-', '-', '-', '-', '-', '-'],e
    #     ['-', '3', '-', '-', '6', '-', '-', '9', '-'],
    #     ['-', '-', '-', '-', '-', '-', 'o', '-', '-'],
    #     # ------------------------------------------------------
    #     ['-', '-', '-', 'x', '-', '-', '-', '-', '-'],
    #     ['-', '2', '-', 'x', '5', '-', '-', '8', '-'],
    #     ['-', '-', '-', 'o', 'o', 'o', '-', '-', '-'],
    #     # ------------------------------------------------------
    #     ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
    #     ['-', '1', '-', '-', '4', '-', '-', '7', '-'],
    #     ['o', '-', '-', 'x', '-', '-', '-', '-', '-']
    # ], depth=2)
    board = Board(depth=3)

    def __init__(self, **kwargs):
        super(BoardWidget, self).__init__(**kwargs)
        self.focus = 0, 0
        self.cursor = []
        self.rect = Rect()
        self.padding = 0.15

    def cgb_zoom(self, touch0, touch1, focus_x, focus_y, delta_scale):
        d = (delta_scale - 1) * 0.4 + 1
        if self.width < min(self.parent.width, self.parent.height) and d < 1:
            return

        rect = Rect(*self.pos, *self.size)
        rect.enlarge(d, (focus_x, focus_y))
        self.size, self.pos = rect.size, rect.pos

    def on_pos(self, *args):
        self.update()

    def on_size(self, *args):
        self.rect.size = self.width, self.width
        self.update()

    def cgb_primary(self, touch, focus_x, focus_y):
        click_rect = Rect(0, 0, self.width, self.width)
        click_pos = focus_x, focus_y
        click_board_pos = []

        for i in range(self.board.depth):
            click_rect.pad(self.padding)
            if click_rect.collide_point(click_pos):
                if click_rect.width < dp(30):
                    return
                w = click_rect.width / 3
                x, y = (click_pos[0] - click_rect.x) // w, (click_pos[1] - click_rect.y) // w
                click_rect = Rect(click_rect.x + x * w, click_rect.y + y * w, w, w)
                click_board_pos.append((int(x), int(y)))
            else:
                return

        valid = self.board.check_valid_move(click_board_pos)
        color = [0, 1, 0, 1] if valid else [1, 0, 0, 1]
        cursor = click_board_pos[1:]
        if valid:
            self.board.play_move(click_board_pos, self.board.turn)
            self.board.switch_turn()
            self.cursor.clear()
            for i in range(len(cursor)):
                if self.board.check_valid_move(cursor[:i + 1]):
                    self.cursor.append(cursor[i])
                else:
                    break

        self.update()
        self.canvas.add(Color(*color))
        self.canvas.add(Line(rectangle=(click_rect.x, click_rect.y, click_rect.width, click_rect.height), width=2))
        Clock.schedule_once(self.update, 2)

    def cgb_select(self, *args):
        self.width = self.height = min(self.parent.width, self.parent.height)
        self.pos = self.parent.center_x - self.width / 2, self.parent.center_y - self.height / 2
        self.selected = True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.focus = touch.x, touch.y
            self.origin = self.x, self.y
            self.move_board = True
        else:
            self.move_board = False

        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.move_board:
            pos = self.pos
            self.x = self.origin[0] + touch.x - self.focus[0]
            self.y = self.origin[1] + touch.y - self.focus[1]

            if not self.collide_widget(self.parent):
                self.pos = pos

        return super().on_touch_move(touch)

    def draw_board_lines_unit(self, x, y, w, color=None, line_width=2):
        if color is None:
            color = [1, 1, 1, 1]  # white line

        box_width = w / 3
        lines = [
            # vertical lines
            (x + box_width, y, x + box_width, y + w),
            (x + box_width * 2, y, x + box_width * 2, y + w),
            # horizontal lines
            (x, y + box_width, x + w, y + box_width),
            (x, y + box_width * 2, x + w, y + box_width * 2)
        ]

        with self.canvas:
            Color(*color)
            for points in lines:
                Line(points=points, width=line_width + 1)

    def draw_board_content_unit(self, x, y, w, board_pos, line_width=2):
        board_unit = self.board.get_unit_board(board_pos)
        padding = self.padding

        for i in range(3):
            for j in range(3):
                sub_w = w / 3
                sub_x = x + sub_w * (padding + i)
                sub_y = y + sub_w * (padding + j)
                sub_w = sub_w * (1 - 2 * padding)
                val = board_unit[2 - j][i]
                if val == X:
                    self.draw_x(sub_x, sub_y, sub_w, line_width=line_width)
                elif val == O:
                    self.draw_o(sub_x, sub_y, sub_w, line_width=line_width)

    def draw_x(self, x, y, w, color=None, line_width=2):
        if color is None:
            color = [1, 0, 0, 1]

        with self.canvas:
            Color(*color)
            Line(points=(x, y, x + w, y + w), width=line_width)
            Line(points=(x, y + w, x + w, y), width=line_width)

    def draw_o(self, x, y, w, color=None, line_width=2):
        if color is None:
            color = [0, 0, 1, 1]

        with self.canvas:
            Color(*color)
            # Line(ellipse=(x + w * 0.3 / 2, y, w * 0.7, w), width=line_width)
            Line(ellipse=(x, y, w, w), width=line_width)

    def draw_win(self, x, y, w, winner, depth):
        if winner != EMPTY:
            with self.canvas:
                Color(0, 0, 0, 0.5)
                Rectangle(pos=(x, y), size=(w, w))
        if winner == X:
            self.draw_x(x, y, w, line_width=depth + 2)
        elif winner == O:
            self.draw_o(x, y, w, line_width=depth + 2)

    def draw_cursor(self):
        def equal(x1, y1, x2, y2):
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 < 0.5

        def get_x(x1, y1, x2, y2, y):
            if y2 - y1 == 0:
                return x1
            return x2 - (y2 - y) * (x2 - x1) / (y2 - y1)

        def get_y(x1, y1, x2, y2, x):
            if (x2 - x1) == 0:
                return y1
            return y2 - (x2 - x) * (y2 - y1) / (x2 - x1)

        cursor = self.cursor
        if len(cursor) == 0:
            return

        main_center = self.rect.center
        rect = self.rect.get_rect_at_pos(cursor)
        rect_center = rect.center
        x, y, w, W = rect.x, rect.y, rect.width, self.width

        shaded_rects = [
            Rect(0, y + w, W, W - w - y),  # top rect
            Rect(0, y, x, w),  # left rect
            Rect(x + w, y, W - w - x, w),  # right rect
            Rect(0, 0, W, y)  # bottom rect
        ]

        self.canvas.add(Color(0, 0, 0, 0.6))
        for shaded_rect in shaded_rects:
            self.canvas.add(Rectangle(pos=shaded_rect.pos, size=shaded_rect.size))
        self.canvas.add(Color(0, 1, 0, 1))
        self.canvas.add(Line(rectangle=(x, y, w, w), width=2))

        if equal(*rect_center, *main_center):
            return

        inclination = math.degrees(math.atan2(main_center[1] - rect_center[1], main_center[0] - rect_center[0]))
        if inclination < 0:
            inclination += 360

        rect_side = int(((inclination - 45) % 360) // 90)
        if rect_side == 0:  # top side
            b_y = y + w
            b_x = get_x(*rect_center, *main_center, b_y)
        elif rect_side == 1:  # left side
            b_x = x
            b_y = get_y(*rect_center, *main_center, b_x)
        elif rect_side == 2:  # bottom side
            b_y = y
            b_x = get_x(*rect_center, *main_center, b_y)
        else:  # right side
            b_x = x + w
            b_y = get_y(*rect_center, *main_center, b_x)

        self.canvas.add(Line(points=(b_x, b_y, *main_center), width=2))


    def draw_board(self, x, y, w, board_pos=None, depth=2, color=None):
        if board_pos is None:
            board_pos = []
        self.draw_board_lines_unit(x, y, w, color=color, line_width=depth)
        padding = self.padding
        if depth > 1:
            # recursely draw content
            for i in range(3):
                for j in range(3):
                    sub_w = w / 3
                    sub_x = x + sub_w * (padding + i)
                    sub_y = y + sub_w * (padding + j)
                    sub_w = sub_w * (1 - 2 * padding)
                    curr_board_pos = board_pos[:]
                    curr_board_pos.append((i, j))
                    self.draw_board(sub_x, sub_y, sub_w, board_pos=curr_board_pos[:], depth=depth - 1, color=color)
        else:
            self.draw_board_content_unit(x, y, w, board_pos)

        winner = self.board.check_win_at(board_pos)
        rect = Rect(x, y, w, w)
        rect.enlarge(1.15)
        self.draw_win(rect.x, rect.y, rect.width, winner, depth)

    def update(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0, 1)
            Rectangle(pos=(0, 0), size=(self.width, self.width))  # background
            Color(0, 1, 103 / 255, 1)
            Line(rectangle=(0, 0, self.width, self.width), width=4)

        rect = Rect(0, 0, self.width, self.width)
        rect.pad(self.padding)
        self.draw_board(rect.x, rect.y, rect.width, depth=self.board.depth, color=[0, 244 / 255, 255 / 255, 1])
        self.draw_cursor()
