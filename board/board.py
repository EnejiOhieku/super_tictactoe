EMPTY = 0
X = +1
O = -1


class Board:
    unit_board = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]

    def __init__(self, board=None, depth=3):
        self.boards = Board.generate_boards(board, depth)
        self.depth = depth
        self.size = 3 ** depth
        self.turn = X

    @property
    def board(self):
        return self.boards[0]

    @staticmethod
    def generate_boards(board=None, depth=2):
        boards = []
        start_depth = depth

        if board is not None:
            start_depth -= 1
            boards.append(board)

        for k in range(start_depth, 0, -1):
            board = []
            for i in range(3 ** k):
                row = []
                for j in range(3 ** k):
                    row.append(EMPTY)
                board.append(row)
            boards.append(board)
        return boards

    @staticmethod
    def slice_board(board, pos, size):
        board = board.copy()
        (x, y), (w, h) = pos, size
        y = len(board) - y - h
        sliced_board = []
        for j in range(y, y + h):
            sliced_board.append(board[j][x: x + w])
        return sliced_board

    def check_valid_move(self, board_pos):
        if Board.check_win_unit(self.boards[-1]):
            return False

        for i in range(len(board_pos)):
            board = self.boards[-i - 1]
            x, y = self.index_from_board_pos(board_pos, i + 1)
            if board[- y - 1][x] != EMPTY:
                return False
        return True

    def index_from_board_pos(self, board_pos, depth=None):
        if depth is None:
            depth = self.depth

        index_x, index_y = 0, 0
        for i, (x, y) in enumerate(board_pos):
            w = 3 ** (depth - i - 1)
            index_x += x * w
            index_y += y * w
        return int(index_x), int(index_y)

    def play_move(self, board_pos, piece):
        for i, board in enumerate(self.boards):
            x, y = self.index_from_board_pos(board_pos, self.depth - i)
            self.boards[i][len(board) - y - 1][x] = piece
            super_board_pos = board_pos[:-(i + 1)]
            super_board = self.get_unit_board(super_board_pos, board)
            piece = self.check_win_unit(super_board)

    def is_empty(self, x, y):
        return self.board[self.size - y - 1][x] == EMPTY

    def switch_turn(self):
        if self.turn == X:
            self.turn = O
        else:
            self.turn = X

    def get_unit_board(self, board_pos, board=None):
        if board is None:
            board = self.board
        depth = int(len(board) ** (1 / 3))
        x, y = self.index_from_board_pos(board_pos, depth)
        w = int(3 ** (depth - len(board_pos)))
        return self.slice_board(board, (x, y), (w, w))

    def check_win_at(self, board_pos):
        if len(board_pos) == 0:
            return self.winner()
        board = self.boards[-len(board_pos)]
        depth = int(len(board) ** (1 / 3))
        x, y = self.index_from_board_pos(board_pos, depth)
        return board[- y - 1][x]

    def winner(self):
        return Board.check_win_unit(self.boards[-1])

    @staticmethod
    def check_win_unit(unit_board):
        # horizontal
        for i in range(3):
            if unit_board[i][0] == unit_board[i][1] == unit_board[i][2] and unit_board[i][0] in [X, O]:
                return unit_board[i][0]
        # vertical
        for i in range(3):
            if unit_board[0][i] == unit_board[1][i] == unit_board[2][i] and unit_board[0][i] in [X, O]:
                return unit_board[0][i]
        # diagonal bottom-top
        if unit_board[0][0] == unit_board[1][1] == unit_board[2][2] and unit_board[1][1] in [X, O]:
            return unit_board[1][1]
        # diagonal top-bottom
        if unit_board[0][2] == unit_board[1][1] == unit_board[2][0] and unit_board[1][1] in [X, O]:
            return unit_board[1][1]
        return EMPTY
