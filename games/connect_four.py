import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algos.adversarial_search import MiniMax
from copy import deepcopy
from collections import Counter


INITIAL_STATE = [
    [None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None],
]


def player_turn_fn(state):
    # X begins first, he's the MAX player
    n_filled = 0
    for row in range(6):
        for col in range(7):
            if state[row][col]:
                n_filled += 1
    return 1 if n_filled % 2 == 0 else -1 

def list_actions_fn(state):
    actions = set({})
    for col in range(7):
        ok = False
        for row in range(6):
            if state[row][col] is None:
                ok = True
        if ok:
            actions.add(col)
    return actions

def take_action_fn(state, action):
    result = deepcopy(state)
    for row in range(5, -1, -1):
        if state[row][action] is None:
            break
    result[row][action] = "X" if player_turn_fn(state) == 1 else "O"
    return result


def utility_fn(state):
    # Check horizontal wins
    for i in range(6):
        for j in range(4):
            cnt = list(Counter(state[i][j:j+4]).keys())
            if len(cnt) == 1 and cnt[0] is not None:
                return 1 if cnt[0] == "X" else -1

    # Check vertical wins
    for j in range(7):
        for i in range(3):
            cnt = list(Counter([state[i+k][j] for k in range(4)]).keys())  # Extract column values
            if len(cnt) == 1 and cnt[0] is not None:
                return 1 if cnt[0] == "X" else -1

    # Check principal diagonal (\) wins
    for i in range(3):
        for j in range(4):
            cnt = list(Counter([state[i+k][j+k] for k in range(4)]).keys())  # Extract diagonal values
            if len(cnt) == 1 and cnt[0] is not None:
                return 1 if cnt[0] == "X" else -1

    # Check secondary diagonal (/) wins
    for i in range(3):
        for j in range(4):
            cnt = list(Counter([state[i+3-k][j+k] for k in range(4)]).keys())# Extract diagonal values
            if len(cnt) == 1 and cnt[0] is not None:
                return 1 if cnt[0] == "X" else -1

    return None  # No winner yet



def heuristic_fn(state):
    score = 0

    # Give points for 2-in-a-row or 3-in-a-row formations
    for i in range(6):
        for j in range(4):
            window = state[i][j:j+4]
            score += evaluate_window(window)

    for j in range(7):
        for i in range(3):
            window = [state[i+k][j] for k in range(4)]
            score += evaluate_window(window)

    for i in range(3):
        for j in range(4):
            window = [state[i+k][j+k] for k in range(4)]
            score += evaluate_window(window)

    for i in range(3):
        for j in range(4):
            window = [state[i+3-k][j+k] for k in range(4)]
            score += evaluate_window(window)

    return score

def evaluate_window(window):
    if window.count("X") == 4:
        return 100  # Winning move for X
    elif window.count("O") == 4:
        return -100  # Winning move for O
    elif window.count("X") == 3 and window.count(None) == 1:
        return 10  # Favorable for X
    elif window.count("O") == 3 and window.count(None) == 1:
        return -10  # Favorable for O
    elif window.count("X") == 2 and window.count(None) == 2:
        return 5  # Slightly good for X
    elif window.count("O") == 2 and window.count(None) == 2:
        return -5  # Slightly good for O
    return 0  # Neutral


def terminal_fn(state):
    return utility_fn(state) is not None

def pretty_print_fn(state):
    print("\n")
    print("     0   1   2   3   4   5   6")
    print("   +---+---+---+---+---+---+---+")
    for i, row in enumerate(state):
        print(f" {i} |", end=" ")
        for cell in row:
            symbol = cell if cell else " "
            print(f"{symbol} |", end=" ")
        print("\n   +---+---+---+---+---+---+---+")



minimax = MiniMax(empty_state = INITIAL_STATE,
                  player_turn_fn = player_turn_fn, 
                  list_actions_fn = list_actions_fn, 
                  take_action_fn = take_action_fn,
                  terminal_fn = terminal_fn,
                  utility_fn = utility_fn, 
                  max_depth = 7,
                  heuristic_fn = heuristic_fn,
                  play_as = 1, 
                  pretty_print_fn = pretty_print_fn)
minimax.game()
