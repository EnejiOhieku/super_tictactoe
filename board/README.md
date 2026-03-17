# Project Overview: Super Tic-Tac-Toe Core Logic

This project implements the backend logic for a "Super" (recursive) Tic-Tac-Toe game. The code is designed to handle a board of arbitrary depth, where winning a smaller inner board acts as a move on the larger outer board.

The logic is encapsulated in a single Python class that manages the state, win conditions, and recursive layers of the game board.

### Key Features

*   **Recursive Board Structure**: Unlike a standard 9x9 fixed array, the board is generated with a configurable `depth`.
    *   **Depth 2**: Standard "Ultimate Tic-Tac-Toe" (9x9 grid composed of nine 3x3 grids).
    *   **Depth 3+**: Fractal expansions of the game.
*   **Layered State Management**: The `Board` class maintains a list of boards (`self.boards`) representing different layers of abstraction.
    *   `self.boards[0]`: The atomic game grid (e.g., the actual pieces X and O).
    *   `self.boards[1+]`: Abstract grids representing the state of won sub-boards.
*   **Win Propagation**: When a move is played, the system checks if a sub-board has been won. If so, that sub-board is marked as "won" by X or O in the layer above, potentially triggering a chain reaction of wins up to the top level.

### Code Breakdown: `board/board.py`

#### Class: `Board`

The central class containing the game state and rules.

**Constants:**
*   `EMPTY = 0`: Represents an empty cell.
*   `X = +1`, `O = -1`: Represent the two players.

**Core Methods:**

*   **`__init__(self, board=None, depth=3)`**:
    Initializes the game. It generates the hierarchy of boards based on the specified depth. The `size` of the raw board is $3^{depth}$.

*   **`generate_boards`**:
    Static method that constructs the layered list of 2D arrays. It creates the raw grid (lowest level) and the "meta" grids (higher levels) that track sub-board victories.

*   **`play_move(self, board_pos, piece)`**:
    Executes a move.
    1.  Calculates the precise index on the detailed board.
    2.  Places the piece.
    3.  Checks `check_win_unit` on the surrounding sub-board.
    4.  If a sub-board is won, it "plays" that win as a piece on the parent board recursively.

*   **`check_valid_move(self, board_pos)`**:
    Verifies if a move is legal. It ensures the game hasn't ended and that the specific cell (and the sub-boards containing it) are not already decided or occupied.

*   **`index_from_board_pos(self, board_pos, depth)`**:
    Converts a hierarchical coordinate path (e.g., "Top-Left quadrant, Center sub-board, Bottom-Right cell") into exact `(x, y)` integer coordinates for the grid at a specific depth.

*   **`check_win_unit(unit_board)`**:
    Standard algorithm to check for a win (horizontal, vertical, or diagonal) on a generic 3x3 grid.

*   **`slice_board`**:
    A utility to extract a specific rectangular section of the board, useful for isolating sub-boards for win checking or display.

### Usage Context

This file serves as the **Model** in an MVC (Model-View-Controller) architecture. It has no dependencies on UI libraries, making it suitable for use with a CLI, GUI (like PyGame or Tkinter), or a web backend.