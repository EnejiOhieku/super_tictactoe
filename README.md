# Super Tic-Tac-Toe

## Project Origin
Developed as a personal project in 200-level second-semester, I built this application with the specific goal of transforming the simple, often predictable game of Tic-Tac-Toe into a complex, multi-layered strategy experience.

## The Concept
Standard Tic-Tac-Toe often ends in a draw and lacks long-term strategic depth. This project implements "Super" (or Recursive) Tic-Tac-Toe to solve that:

*   **Fractal Gameplay**: The game board is recursive. Each cell in the main board contains a smaller Tic-Tac-Toe board.
*   **Strategic Constraint**: The move you make in a small inner board dictates which specific board your opponent must play in next. This forces players to think globally while acting locally.
*   **Win Propagation**: Winning a small board claims that cell on the larger board. The goal is to win the "Meta" board.

## Technical Overview
The project is built using **Python** with a clean separation between the recursive game logic and the graphical user interface.

### Tech Stack
*   **Language**: Python 3



*   **GUI Framework**: Kivy & KivyMD (Material Design)

### Demo

[Recursive depth 2](https://github.com/user-attachments/assets/c407055c-9b5b-4ac7-9398-5eb1aa2c4b1d)

[Recursive depth 3](https://github.com/user-attachments/assets/29bf42b0-741b-48ed-ac93-a12523f8424f)

### Core Logic (`board/board.py`)
The backend features a robust `Board` class capable of handling arbitrary depths (e.g., Depth 2 for standard Ultimate Tic-Tac-Toe, Depth 3+ for fractal expansions) [read more](board/README.md).
*   **State Management**: Maintains a hierarchy of boards, tracking the state of the raw grid and the abstract "won" grids simultaneously.
*   **Recursive Validation**: Automatically calculates valid moves based on the previous player's action in the sub-grids.

## Getting Started

### Prerequisites
You will need Python installed along with the Kivy framework.

```bash
pip install kivy kivymd gestures4kivy
```

### Running the Game
Execute the main script to launch the GUI window.

```bash
python main.py



```
