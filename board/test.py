def slice_board(board, pos, size):
    board = board.copy()

    (x, y), (w, h) = pos, size
    y = len(board) - y - 1

    assert h - 1 <= y < len(board) and x + w < len(board[0]), "Invalid Slice operation"

    sliced_board = []
    for j in range(y, y - h, -1):
        sliced_board.append(board[j][x : x + w])
    sliced_board.reverse()
    return sliced_board

board = [
        ['x', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '3', '-', '-', '6', '-', '-', '9', '-'],
        ['-', '-', '-', '-', '-', '-', 'o', '-', '-'],
        # ------------------------------------------------------
        ['-', '-', '-', 'x', '-', '-', '-', '-', '-'],
        ['-', '2', '-', 'x', '5', '-', '-', '8', '-'],
        ['-', '-', '-', 'o', 'o', 'o', '-', '-', '-'],
        # ------------------------------------------------------
        ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '1', '-', '-', '4', '-', '-', '7', '-'],
        ['o', '-', '-', 'x', '-', '-', '-', '-', '-']
    ]
print(slice_board(board, (0, 1), (3, 3)))