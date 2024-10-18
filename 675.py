import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.center_window(340, 350)
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def center_window(self, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    self.root,
                    text=" ",
                    font=("Arial", 40),
                    width=3,
                    height=1,
                    command=lambda row=i, col=j: self.button_click(row, col)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

    def button_click(self, row, col):
        if self.game_over:
            return

        if self.board[row][col] != '':
            return

        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player)

        if self.win(self.current_player):
            self.game_over = True
            self.show_winner(self.current_player)
        elif self.draw():
            self.game_over = True
            self.show_winner("Ничья")
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if self.current_player == 'O':
                self.computer_move()

    def computer_move(self):
        available_moves = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == '']
        best_score = float('-inf')
        best_move = None

        for row, col in available_moves:
            self.board[row][col] = 'O'
            score = self.best_move(self.board, False)
            self.board[row][col] = ''
            if score > best_score:
                best_score = score
                best_move = (row, col)

        if best_move is not None:
            row, col = best_move
            self.button_click(row, col)

    def win(self, player):
        for i in range(3):
            if self.board[i][0] == player and self.board[i][1] == player and self.board[i][2] == player:
                return True
            if self.board[0][i] == player and self.board[1][i] == player and self.board[2][i] == player:
                return True
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            return True
        if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
            return True
        return False

    def draw(self):
        return all(self.board[row][col] != '' for row in range(3) for col in range(3))

    def best_move(self, board, is_player_move):
        if self.win('O'):
            return 1
        elif self.win('X'):
            return -1
        elif self.draw():
            return 0

        available_moves = [(row, col) for row in range(3) for col in range(3) if board[row][col] == '']

        if is_player_move:
            best_score = float('-inf')
            for row, col in available_moves:
                board[row][col] = 'O'
                score = self.best_move(board, False)
                board[row][col] = ''
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in available_moves:
                board[row][col] = 'X'
                score = self.best_move(board, True)
                board[row][col] = ''
                best_score = min(score, best_score)
            return best_score

    def show_winner(self, winner):
        if winner == "Ничья":
            messagebox.showinfo("Результат", "Ничья!")
        else:
            messagebox.showinfo("Результат", f"Победил {winner}!")
        self.restart()

    def restart(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
