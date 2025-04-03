import ast
import time

class MiniMax:
    """
    A modular implementation of MiniMax algorithm for adversarial games against an AI.
    If you play optimally, you will pull off a draw, otherwise the AI will always defeat you.
    Unless depth limiting is employed, in which case you might be able to win.
    """

    def __init__(self,
                 empty_state,
                 player_turn_fn: callable,
                 list_actions_fn: callable,
                 take_action_fn: callable,
                 terminal_fn: callable,
                 utility_fn: callable,
                 max_depth = None,
                 heuristic_fn: callable = None,
                 pretty_print_fn = print,
                 play_as = -1,
        ):
        """
        Parameters:
        ------------
        - player_turn_fn (callable): A function that takes in a state and 
        returns who's player turn is next (+1 for the MAX player, -1 for the MIN player).
        - list_actions_fn (callable): Function that takes in a state and 
        returns a set of all the possible next actions. If action type is custom
        class, make sure it has a  __repr__ method for proper player input eval.
        - take_action (callable): Function that takes in a state, an 
        action and returns the result state.
        - terminal_fn (callable): Function that takes in a state and verifies
        if it is a terminal state, returning a boolean.
        - utility_fn (callable): A function that takes in an end state
        and returns its utility numerical value (+1, 0, -1). The MAX player aims to maximize
        the utility, while the MIN player has the opposite goal.   
        - max_depth (int): Parameter used to limit recursion depth. Default is None (no limit).
        - heuristic_fn (callable): A function that takes in as input a non-terminal state and
        calculates the most likely winner. Returns a real-valued score, where higher score
        means MAX player is more likely to win the game.
        Used when depth limit is on.
        - empty_state: Environment's state in the beginning.
        - pretty_print_fn (callable): Optional function for printing state 
        during the game. Default is normal print. 
        - plays_as: 1 for MAX player, -1 for MIN. 
        """
        self.empty_state = empty_state
        self.player_turn_fn = player_turn_fn
        self.list_actions_fn = list_actions_fn
        self.take_action_fn = take_action_fn
        self.terminal_fn = terminal_fn
        self.utility_fn = utility_fn
        self.max_depth = max_depth
        self.heuristic_fn = heuristic_fn
        self.play_as = play_as
        self.pretty_print_fn = pretty_print_fn
        self.states_history = []
        

    
    def min(self, state, alpha=float("-inf"), k=None):
        if k == 0:
            return self.heuristic_fn(state), None
        if self.terminal_fn(state):
            return self.utility_fn(state), None
        minn, action_minn = float("inf"), None
        for action in self.list_actions_fn(state):
            result_state = self.take_action_fn(state, action)
            optimal_play, _ = self.max(result_state, minn, k=(None if k is None else k-1))
            if optimal_play < minn:
                minn = optimal_play
                action_minn = action
            if minn <= alpha:
                break
        return minn, action_minn


    def max(self, state, beta=float("inf"), k=None):
        if k == 0:
            return self.heuristic_fn(state), None
        if self.terminal_fn(state):
            return self.utility_fn(state), None
        maxx, action_maxx = float("-inf"), None
        for action in self.list_actions_fn(state):
            result_state = self.take_action_fn(state, action)
            optimal_play, _ = self.min(result_state, maxx, k=(None if k is None else k-1))
            if optimal_play > maxx:
                maxx = optimal_play
                action_maxx = action
            if maxx >= beta:
                break
        return maxx, action_maxx
    
    def game(self):
        print("\n\nStarting the adversarial MiniMax game.")
        print(f"You are the {'MAX' if self.play_as == 1 else 'MIN'} player.")
        current_state = self.empty_state
        self.states_history = [current_state]
        print(f"Starting state:\n")
        self.pretty_print_fn(current_state)
        while not self.terminal_fn(current_state):
            if self.play_as == self.player_turn_fn(current_state):
                possible_actions = list(self.list_actions_fn(current_state))
                print(f"\nIt's your turn. Pick one of the following possible actions:\n"
               f"{possible_actions}.")
                while True:
                    try:
                        action_str = input("\nEnter your action: ")
                        chosen_action = ast.literal_eval(action_str)
                        if chosen_action in possible_actions:
                            break
                        else:
                            print("That's not a valid action. Try again.")
                    except (ValueError, SyntaxError):
                        print("Invalid input format. Please try again.")
                current_state = self.take_action_fn(current_state, chosen_action)
            else:
                time.sleep(1)
                print("\nIt's the AI's turn.")
                _, action = (self.max(current_state, k=self.max_depth) if self.play_as == -1 
                             else self.min(current_state, k=self.max_depth)) 
                print(f"AI chose action: {action}.")
                current_state = self.take_action_fn(current_state, action)
            print(f"New state:\n")
            self.pretty_print_fn(current_state)
            self.states_history.append(current_state)
        
        end_utility = self.utility_fn(current_state)
        print("\n\n")
        if end_utility == 0:
            print("Draw! 😄")
        elif self.play_as == end_utility:
            print("Congratulations! You won the game! 😄")
        elif end_utility is not None:
            print("Tough luck! The AI won this time! 😈")
        if input("Do you want to play again? YES / NO? ").lower() == "yes":
            self.game()
