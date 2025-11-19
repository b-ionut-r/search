# Add this at the top of tictactoe.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algos.adversarial_search import MiniMax
from copy import deepcopy
import tkinter as tk
from tkinter import messagebox
from tkinter import font

INITIAL_STATE = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]


def player_turn_fn(state):
    # X begins first, he's the MAX player
    n_filled = 0
    for row in range(3):
        for col in range(3):
            if state[row][col]:
                n_filled += 1
    return 1 if n_filled % 2 == 0 else -1 

def list_actions_fn(state):
    actions = []
    for row in range(3):
        for col in range(3):
            if state[row][col] is None:
                actions.append((row, col))
    return actions

def take_action_fn(state, action):
    result = deepcopy(state)
    result[action[0]][action[1]] = "X" if player_turn_fn(state) == 1 else "O"
    return result


def utility_fn(state):
    for i in range(3):  # Check rows
        if state[i][0] is not None and state[i][0] == state[i][1] == state[i][2]:
            return 1 if state[i][0] == "X" else -1
    for j in range(3):  # Check columns
        if state[0][j] is not None and state[0][j] == state[1][j] == state[2][j]:
            return 1 if state[0][j] == "X" else -1
    # Check diagonals
    if state[1][1] is not None:  
        if state[0][0] == state[1][1] == state[2][2]:
            return 1 if state[1][1] == "X" else -1
        if state[0][2] == state[1][1] == state[2][0]:
            return 1 if state[1][1] == "X" else -1
    # Check for empty spaces
    for i in range(3):
        for j in range(3):
            if state[i][j] is None:
                return None  # Game not over yet
    return 0  # Draw

def terminal_fn(state):
    return utility_fn(state) is not None

def pretty_print_fn(state):
    print("\n")
    print("     0   1   2")
    print("   +---+---+---+")
    for i, row in enumerate(state):
        print(f" {i} |", end=" ")
        for cell in row:
            symbol = cell if cell else " "
            print(f"{symbol} |", end=" ")
        print("\n   +---+---+---+")


# Custom MiniMax class with minimax_decision method
class MiniMaxTicTacToe(MiniMax):
    def minimax_decision(self, state):
        """
        Returns the best action for the current player using minimax algorithm.
        """
        actions = self.list_actions_fn(state)
        
        if not actions:
            return None
            
        player = self.player_turn_fn(state)
        
        if player == 1:  # MAX player
            best_score = float('-inf')
            best_action = None
            
            for action in actions:
                next_state = self.take_action_fn(state, action)
                score = self.min_value(next_state)
                
                if score > best_score:
                    best_score = score
                    best_action = action
        else:  # MIN player
            best_score = float('inf')
            best_action = None
            
            for action in actions:
                next_state = self.take_action_fn(state, action)
                score = self.max_value(next_state)
                
                if score < best_score:
                    best_score = score
                    best_action = action
                    
        return best_action
    
    def max_value(self, state):
        if self.terminal_fn(state):
            return self.utility_fn(state)
            
        value = float('-inf')
        
        for action in self.list_actions_fn(state):
            next_state = self.take_action_fn(state, action)
            value = max(value, self.min_value(next_state))
            
        return value
        
    def min_value(self, state):
        if self.terminal_fn(state):
            return self.utility_fn(state)
            
        value = float('inf')
        
        for action in self.list_actions_fn(state):
            next_state = self.take_action_fn(state, action)
            value = min(value, self.max_value(next_state))
            
        return value


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        self.current_state = deepcopy(INITIAL_STATE)
        self.human_player = 1  # X is human (MAX player)
        self.ai_player = -1    # O is AI (MIN player)
        
        # Initialize MiniMaxTicTacToe algorithm instead of MiniMax
        self.minimax = MiniMaxTicTacToe(
            empty_state=INITIAL_STATE,
            player_turn_fn=player_turn_fn,
            list_actions_fn=list_actions_fn,
            take_action_fn=take_action_fn,
            terminal_fn=terminal_fn,
            utility_fn=utility_fn,
            play_as=self.ai_player,  # AI plays as O
            pretty_print_fn=pretty_print_fn
        )
        
        # Create game status label
        self.status_font = font.Font(size=14, weight="bold")
        self.status_label = tk.Label(
            self.root, 
            text="Your turn (X)", 
            font=self.status_font,
            bg="#b73e3e"
        )
        self.status_label.pack(pady=10)
        
        # Create game board frame
        self.board_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.board_frame.pack(pady=10)
        
        # Create buttons for the board
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.button_font = font.Font(size=24, weight="bold")
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.board_frame,
                    text="",
                    font=self.button_font,
                    width=3,
                    height=1,
                    command=lambda row=i, col=j: self.make_move(row, col)
                )
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)
        
        # Create reset button
        self.reset_button = tk.Button(
            self.root,
            text="New Game",
            font=font.Font(size=12),
            command=self.reset_game,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.reset_button.pack(pady=20)
    
    def make_move(self, row, col):
        # Check if cell is empty and game not over
        if self.current_state[row][col] is not None or terminal_fn(self.current_state):
            return
            
        # Human move
        self.current_state = take_action_fn(self.current_state, (row, col))
        self.update_board()
        
        # Check if game is over after human move
        if terminal_fn(self.current_state):
            self.end_game()
            return
            
        # AI move
        self.status_label.config(text="AI is thinking...")
        self.root.update()
        
        action = self.minimax.minimax_decision(self.current_state)
        self.current_state = take_action_fn(self.current_state, action)
        self.update_board()
        
        # Check if game is over after AI move
        if terminal_fn(self.current_state):
            self.end_game()
        else:
            self.status_label.config(text="Your turn (X)")
    
    def update_board(self):
        for i in range(3):
            for j in range(3):
                if self.current_state[i][j] == "X":
                    self.buttons[i][j].config(text="X", fg="#FF5722")
                elif self.current_state[i][j] == "O":
                    self.buttons[i][j].config(text="O", fg="#2196F3")
    
    def end_game(self):
        result = utility_fn(self.current_state)
        if result == 1:
            self.status_label.config(text="You win!")
            messagebox.showinfo("Game Over", "Congratulations! You win!")
        elif result == -1:
            self.status_label.config(text="AI wins!")
            messagebox.showinfo("Game Over", "AI wins! Better luck next time.")
        else:
            self.status_label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
    
    def reset_game(self):
        self.current_state = deepcopy(INITIAL_STATE)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        self.status_label.config(text="Your turn (X)")

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
