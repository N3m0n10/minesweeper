import tkinter as tk
import random

# Color map for numbers (like the real Minesweeper)
COLORS = {
    "1": "blue", "2": "green", "3": "red", "4": "dark blue",
    "5": "brown", "6": "cyan", "7": "black", "8": "gray"
}

class Minesweeper:
    def __init__(self, root, size=8, mines=10):
        self.root = root
        self.size = size
        self.mines = mines
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.mine_positions = set()
        self.revealed = set()
        self.flags = set()
        self.buttons = [[None for _ in range(size)] for _ in range(size)]

        self.header_frame = tk.Frame(root)
        self.header_frame.pack()
        
        self.game_frame = tk.Frame(root)
        self.game_frame.pack()

        self.create_header()
        self.start_game()

    def create_header(self):
        tk.Button(self.header_frame, text="Restart 🔄", font=("Arial", 12), command=self.restart).grid(row=0, column=0)
        tk.Button(self.header_frame, text="Easy 😊", font=("Arial", 12), command=lambda: self.change_difficulty(8, 10)).grid(row=0, column=1)
        tk.Button(self.header_frame, text="Hard 🔥", font=("Arial", 12), command=lambda: self.change_difficulty(12, 30)).grid(row=0, column=2)

    def start_game(self):
        self.place_mines()
        self.calculate_numbers()
        self.create_ui()

    def place_mines(self):
        self.mine_positions.clear()
        while len(self.mine_positions) < self.mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.mine_positions.add((x, y))

    def calculate_numbers(self):
        for x, y in self.mine_positions:
            self.board[x][y] = 'M'
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] != 'M':
                        self.board[nx][ny] = str(int(self.board[nx][ny]) + 1) if self.board[nx][ny] != ' ' else '1'

    def create_ui(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                btn = tk.Button(self.game_frame, text=" ", width=3, height=1, font=("Arial", 14), 
                                command=lambda x=i, y=j: self.reveal(x, y))
                btn.bind("<Button-3>", lambda event, x=i, y=j: self.toggle_flag(x, y))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def reveal(self, x, y):
        if (x, y) in self.flags or (x, y) in self.revealed:
            return

        if self.board[x][y] == 'M':
            self.buttons[x][y].config(text="💥", bg="red")
            self.game_over(False)
            return

        self.revealed.add((x, y))
        num = self.board[x][y]
        self.buttons[x][y].config(
            text=num if num != ' ' else "", 
            bg="light gray",
            fg=COLORS.get(num, "black") if num in COLORS else "black"
        )

        if num == ' ':
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                        self.reveal(x + dx, y + dy)

        if len(self.revealed) == self.size * self.size - self.mines:
            self.game_over(True)

    def toggle_flag(self, x, y):
        if (x, y) in self.revealed:
            return
        if (x, y) in self.flags:
            self.flags.remove((x, y))
            self.buttons[x][y].config(text=" ")
        else:
            self.flags.add((x, y))
            self.buttons[x][y].config(text="💣")

    def game_over(self, won):
        for x, y in self.mine_positions:
            self.buttons[x][y].config(text="💣")
        msg = "🎉 You Won! 🎉" if won else "💀 Game Over! You hit a mine!"
        result = tk.Label(self.game_frame, text=msg, font=("Arial", 16))
        result.grid(row=self.size, column=0, columnspan=self.size)

    def restart(self):
        self.revealed.clear()
        self.flags.clear()
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.start_game()

    def change_difficulty(self, size, mines):
        self.size = size
        self.mines = mines
        self.restart()

# Start the game
root = tk.Tk()
root.title("Minesweeper")
game = Minesweeper(root)
root.mainloop()
