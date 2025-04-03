import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algos.adversarial_search import MiniMax
from copy import deepcopy

INITIAL_STATE = [
    [None for _ in range(6)] for _ in range(6)
]

def player_turn_fn(state):
    n_filled = sum(1 for row in state for cell in row if cell is not None)
    return 1 if n_filled % 2 == 0 else -1

def list_actions_fn(state):
    actions = {(row, col)
               for row in range(len(state))
               for col in range(len(state[0]))
               if state[row][col] is None}
    return actions

def take_action_fn(state, action):
    result = deepcopy(state)
    row, col = action
    result[row][col] = "X" if player_turn_fn(state) == 1 else "O"
    return result

def utility_fn(state):
    # A complete 2x2 square wins.
    for i in range(len(state) - 1):
        for j in range(len(state[0]) - 1):
            square = [
                state[i][j], state[i][j+1],
                state[i+1][j], state[i+1][j+1]
            ]
            if all(cell == "X" for cell in square):
                return 1
            if all(cell == "O" for cell in square):
                return -1
    # Draw if full board and no win.
    if all(cell is not None for row in state for cell in row):
        return 0
    return None  # Game not over

def heuristic_fn(state):
    score = 0
    # Iterate through each possible 2x2 square
    for i in range(len(state) - 1):
        for j in range(len(state[0]) - 1):
            square = [
                state[i][j], state[i][j+1],
                state[i+1][j], state[i+1][j+1]
            ]
            x = square.count("X")
            o = square.count("O")
            # Score squares where the player can potentially complete a 2x2
            if x > 0 and o == 0:
                # Use exponential scoring to prioritize squares closer to completion
                score += x * x * x
            elif o > 0 and x == 0:
                score -= o * o * o
    return score

def terminal_fn(state):
    return utility_fn(state) is not None

def pretty_print_fn(state):
    print("\n     0   1   2   3   4   5")
    print("   +---+---+---+---+---+---+")
    for i, row in enumerate(state):
        print(f" {i} |", end=" ")
        for cell in row:
            symbol = cell if cell else " "
            print(f"{symbol} |", end=" ")
        print("\n   +---+---+---+---+---+---+")

# Optionally increase max_depth for a 6x6 grid.
minimax = MiniMax(empty_state=INITIAL_STATE,
                  player_turn_fn=player_turn_fn, 
                  list_actions_fn=list_actions_fn, 
                  take_action_fn=take_action_fn,
                  terminal_fn=terminal_fn,
                  utility_fn=utility_fn, 
                  max_depth=5,  # increased from 4
                  heuristic_fn=heuristic_fn,
                  play_as=1, 
                  pretty_print_fn=pretty_print_fn)
minimax.game()
