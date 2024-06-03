import tkinter as tk
from tkinter import messagebox, colorchooser

class TicTacToe:
    def __init__(self, root, x_color="black", o_color="red"):
        """Initialize the Tic Tac Toe game."""
        self.root = root
        self.root.title("Tic Tac Toe")
        self.is_player_turn = True  # Player starts the game
        self.current_player = "X"  # Current player starts as "X"
        self.x_color = x_color  # Color for X
        self.o_color = o_color  # Color for O
        self.board = [""] * 9
        self.buttons = []
        self.create_board()

    def create_board(self):
        """Create the game board."""
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                button = tk.Button(self.root, text="", font=("Arial", 24), width=5, height=2,
                                   command=lambda idx=index: self.player_move(idx))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)
        reset_button = tk.Button(self.root, text="Restart", font=("Arial", 16), bg="lightgray", fg="black",
                                 command=self.reset_board)
        reset_button.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=10)

    def player_move(self, index):
        """Handle player's move."""
        if self.board[index] == "" and self.is_player_turn:
            self.make_move(index, self.current_player)
            if not self.check_game_over():
                self.switch_player()  # Switch player after player's move
                self.is_player_turn = False
                self.root.after(500, self.computer_move)

    def computer_move(self):
        """Handle computer's move."""
        if not self.is_player_turn:
            move = self.find_best_move()
            if move != -1:
                self.make_move(move, "O")
                if not self.check_game_over():
                    self.switch_player()  # Switch player after computer's move
                    self.is_player_turn = True  # Allow player to move again

    def make_move(self, index, player):
        """Make a move on the board."""
        self.board[index] = player
        self.buttons[index].config(text=player, fg=self.x_color if player == "X" else self.o_color)

    def switch_player(self):
        """Switch the current player."""
        self.current_player = "X" if self.current_player == "O" else "O"

    def find_best_move(self):
        """Find the best move for the computer."""
        # Basic strategy for Tic-Tac-Toe
        # 1. Check for a win
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_win():
                    self.board[i] = ""  # Reset to empty for the actual move
                    return i
                self.board[i] = ""  # Reset if not winning

        # 2. Block opponent's win
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_win():
                    self.board[i] = ""  # Reset to empty for the actual move
                    return i
                self.board[i] = ""  # Reset if not a block

        # 3. Take the center if available
        if self.board[4] == "":
            return 4

        # 4. Take any opposite corner if the opponent is in a corner
        corners = [(0, 8), (2, 6)]
        for own, opp in corners:
            if self.board[own] == "X" and self.board[opp] == "":
                return opp
            elif self.board[opp] == "X" and self.board[own] == "":
                return own

        # 5. Take any empty corner
        for i in [0, 2, 6, 8]:
            if self.board[i] == "":
                return i

        # 6. Take any empty side
        for i in [1, 3, 5, 7]:
            if self.board[i] == "":
                return i

        return -1  # No move found (should not happen)

    def check_game_over(self):
        """Check if the game is over."""
        if self.check_win() or all(spot != "" for spot in self.board):
            result = "Draw" if not self.check_win() else f"Player {self.current_player} wins!"
            messagebox.showinfo("Game Over", result)
            self.reset_board()
            return True
        return False

    def check_win(self):
        """Check if a player has won."""
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return True
        return False

    def reset_board(self):
        """Reset the game board."""
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="", fg="black")
        self.current_player = "X"
        self.is_player_turn = True

class MainMenu:
    def __init__(self, root):
        """Initialize the main menu."""
        self.root = root
        self.root.title("Tic Tac Toe")

        # Customizing main menu appearance
        self.root.geometry("300x300")
        self.root.configure(bg="lightgray")

        tk.Label(root, text="Tic Tac Toe", font=("Arial", 20), bg="lightgray").pack(pady=20)

        play_btn = tk.Button(root, text="Play Against Computer", font=("Arial", 16), bg="gray", fg="white",
                             command=self.start_game)
        play_btn.pack(fill="x", padx=50, pady=10)

    def start_game(self):
        """Start the Tic Tac Toe game."""
        game_window = tk.Toplevel()
        game_window.title("Tic Tac Toe")
        game_window.geometry("370x380")
        game_window.configure(bg="lightgray")
        TicTacToe(game_window)

def open_tic_tac_app():
    """Open the Tic Tac Toe application."""
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    open_tic_tac_app()
