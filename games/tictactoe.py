# Add this at the top of tictactoe.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algos.adversarial_search import MiniMax
from copy import deepcopy

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



minimax = MiniMax(empty_state = INITIAL_STATE,
                  player_turn_fn = player_turn_fn, 
                  list_actions_fn = list_actions_fn, 
                  take_action_fn = take_action_fn,
                  terminal_fn = terminal_fn,
                  utility_fn = utility_fn, 
                  play_as = 1, 
                  pretty_print_fn = pretty_print_fn)
minimax.game()