import math

class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost."""

    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given state."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given action."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 via
        state1 then action, assuming cost c to get up to state1."""
        return c + 1

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return f"<Node {self.state}>"

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """Create a child node from an action."""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action,
                         problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __lt__(self, node):
        """Used for tie-breaking in PriorityQueue."""
        return self.state < node.state