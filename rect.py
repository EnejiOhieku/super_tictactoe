class Rect:

    def __init__(self, left=0.0, bottom=0.0, width=0.0, height=0.0):
        self.x = left
        self.y = bottom
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def pos(self):
        return self.x, self.y

    @property
    def size(self):
        return self.width, self.height

    @property
    def center(self):
        return self.x + self.width / 2, self.y + self.height / 2

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

    @size.setter
    def size(self, value):
        self.width, self.height = value

    def collide_point(self, point):
        x1, y1 = point
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height

    def pad(self, padding):
        self.x, self.y = self.x + self.width * padding, self.y + self.height * padding
        self.width, self.height = self.width * (1 - 2 * padding), self.height * (1 - 2 * padding)

    def enlarge(self, d, focus=None):
        if focus is None:
            focus = self.width / 2, self.height / 2
        focus_x, focus_y = focus
        tx, ty = self.x + focus_x, self.y + focus_y
        self.size = (self.width * d, self.height * d)
        self.pos = tx - focus_x * d, ty - focus_y * d

    @property
    def list(self):
        return self.x, self.y, self.width, self.height

    def get_rect_at_pos(self, board_pos, padding=0.15):
        rect = Rect()
        rect.pos, rect.size = self.pos, self.size

        for x, y in board_pos:
            rect.pad(padding)
            w = rect.width / 3
            rect = Rect(rect.x + x * w, rect.y + y * w, w, w)
        return rect
