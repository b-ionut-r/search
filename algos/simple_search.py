class Node:
    """
    A data structure that keeps track of:
    - a state
    - a parent (node that generated this node)
    - an action (action applied on parent to get node)
    - a path cost (from initial state to node)
    """
    def __init__(self, state, parent=None, action=None, cost=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.is_root_node = True if parent is None else False
        self.is_leaf_node = False 
        self.heur_val = None


    def expand(self, list_actions: callable, take_action: callable) -> set:
        """
        Expands the node, i.e returns a set of all possible
        nodes that the agent can explore from the current node.
        """
        possible_actions = list_actions(self.state)
        nodes = set({})
        for action in possible_actions:
            new_state, step_cost = take_action(self.state, action)
            new_node = Node(new_state, self, action, self.cost + step_cost)
            nodes.add(new_node)
        if not nodes:
            self.is_leaf_node = True
        return nodes
    
    def check_goal_state(self, goal_checker: callable):
        return goal_checker(self.state)
        


class Frontier:
    """
    A data structure that contains current exploration options,
    as well as a history of all explored nodes.
    """
    def __init__(self, nodes):
        assert all([isinstance(node, Node) for node in nodes]), \
        "Please provide an iterable of nodes."
        self.nodes = list(nodes)  # Using a list to maintain order
        self.history = set()  # Set for efficient lookup in history
           
    def remove(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            self.history.add(node)
    
    def extend(self, nodes):
        # Add only nodes that aren't already in the frontier
        for node in nodes:
            if node not in self.nodes:
                self.nodes.append(node)
    
    def fifo(self):
        """First In, First Out - returns the oldest node in the frontier."""
        try:
            return self.nodes[0] if self.nodes else None
        except IndexError:
            return None
    
    def lifo(self):
        """Last In, First Out - returns the newest node in the frontier."""
        try:
            return self.nodes[-1] if self.nodes else None
        except IndexError:
            return None
        
    def guess(self, heuristic):
        """Samples closest node according to heuristic function."""
        minn, node_minn = float("inf"), None
        for node in self.nodes:
            if not node.heur_val:
                node.heur_val = heuristic(node.state)
            if node.heur_val < minn:
                minn = node.heur_val
                node_minn = node
        return node_minn
    
    def a_star_guess(self, heuristic):
        """Samples the node with lowest value of path cost to current state
        plus estimated cost"""
        minn, node_minn = float("inf"), None
        for node in self.nodes:
            if not node.heur_val:
                node.heur_val = heuristic(node.state) + node.cost
            if node.heur_val < minn:
                minn = node.heur_val
                node_minn = node
        return node_minn

    def __len__(self):
        return len(self.nodes)



class Search:
    """
    Depth First Search / Breadth First Search Algorithms
    """
    def __init__(self,
                 start_state,
                 list_actions: callable,
                 take_action: callable,
                 goal_checker: callable,
                 algo = "bfs",
                 heuristic: callable = None):
        """
        A modular implementation of various search algorithms.

        Parameters:
        ------------
        - start_state: The state of the agent in the beginging.
        - list_actions (callable): Function that takes in a state and 
        returns a set of all possible actions the agent can take next.
        - take_action (callable): Function that takes in a state, an 
        action and returns the result state, along with a step cost.
        - goal_checker (callable): Function that takes in a state and verifies
        if it is the goal state, returning a boolean.
        - algo (str): One of the following options:
            * "dfs": Depth First Search
            * "bfs": Breadth First Search
            * "gbf": Greedy Best First Search
            * "a*": A* Search
        - heuristic (callable, optional): Function that takes in a state and computes
        a measure of closeness to the end goal. Needed for "gbf" and "A*" algorithms.
        """
        if algo == "gbf":
            assert heuristic , "You must provide a heuristic function to guide the frontier sampling"
            "when using greedy-best search algorithm."
        self.start = Node(start_state, cost=0)
        self.list_actions = list_actions
        self.take_action = take_action
        self.goal_checker = goal_checker
        self.frontier = Frontier({self.start})
        self.algo = algo
        self.heuristic = heuristic
        self.sample_mapping = {
                "dfs": self.frontier.lifo,
                "bfs": self.frontier.fifo,
                "gbf": lambda: self.frontier.guess(self.heuristic),
                "a*": lambda: self.frontier.a_star_guess(self.heuristic),
        }


    def search(self):
        current_node = self.start
        while self.frontier and not current_node.check_goal_state(self.goal_checker):
            current_node = self.sample_mapping.get(self.algo, lambda: None)() # sample node based on algo
            if current_node in self.frontier.history:
                continue
            new_nodes = current_node.expand(self.list_actions, self.take_action)
            self.frontier.remove(current_node)
            self.frontier.extend(new_nodes)

        if current_node.check_goal_state(self.goal_checker):
            path = [current_node]
            total_cost = current_node.cost
            while current_node.parent:
                current_node = current_node.parent
                path.append(current_node)
            return reversed(path), total_cost
        return None 