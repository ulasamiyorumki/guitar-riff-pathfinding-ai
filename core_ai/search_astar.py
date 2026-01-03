import heapq
import itertools
from core_ai.models import Problem, Node
from core_ai.note_mapping import NoteMapper
from core_ai.cost import ErgonomicCost


class GuitarPathProblem(Problem):
    """
    Solves the guitar pathfinding task using A* with optimality guarantees.
    State format: (string, fret, note_index)
    """

    def __init__(self, riff_notes):
        self.mapper = NoteMapper()
        self.cost_calculator = ErgonomicCost()
        self.riff_notes = riff_notes

        # Dummy initial state (before first note)
        initial_state = (0, 0, -1)
        super().__init__(initial_state)

    def actions(self, state):
        string, fret, note_index = state
        next_index = note_index + 1

        if next_index >= len(self.riff_notes):
            return []

        next_note = self.riff_notes[next_index]
        midi_val = self.mapper.note_to_midi(next_note)

        if midi_val is None:
            return []

        positions = self.mapper.find_positions_on_fretboard(midi_val)
        return [(s, f, next_index) for s, f in positions]

    def result(self, state, action):
        return action

    def goal_test(self, state):
        return state[2] == len(self.riff_notes) - 1

    def path_cost(self, c, state1, action, state2):
        # Small base cost for first note (instead of free teleport)
        if state1[2] == -1:
            return c + 1.0

        pos1 = (state1[0], state1[1])
        pos2 = (state2[0], state2[1])

        step_cost = self.cost_calculator.calculate_step_cost(pos1, pos2)

        # Soft anatomical constraint
        if not self.cost_calculator.is_physically_possible(pos1, pos2):
            step_cost += 15.0

        return c + step_cost

    def h(self, node):
        """
        Admissible heuristic:
        Minimum possible cost assuming best-case movement.
        """
        remaining_notes = len(self.riff_notes) - 1 - node.state[2]
        MIN_STEP_COST = 1.0
        return remaining_notes * MIN_STEP_COST


def astar_search(problem):
    """
    Correct A* implementation with dominance checks.
    """

    start = Node(problem.initial)

    counter = itertools.count()
    frontier = []
    heapq.heappush(frontier, (problem.h(start), next(counter), start))

    # Best known g(n) for each state
    best_g = {start.state: 0}

    while frontier:
        _, _, node = heapq.heappop(frontier)

        if problem.goal_test(node.state):
            return node.path()

        for child in node.expand(problem):
            s = child.state
            g = child.path_cost

            # Dominance check (KEY FIX)
            if s not in best_g or g < best_g[s]:
                best_g[s] = g
                f = g + problem.h(child)
                heapq.heappush(frontier, (f, next(counter), child))

    return None
