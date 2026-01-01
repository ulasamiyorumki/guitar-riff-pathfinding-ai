from core_ai.models import Problem
from core_ai.note_mapping import NoteMapper
from core_ai.cost import ErgonomicCost


class GuitarPathProblem(Problem):
    """
    Solves the guitar pathfinding task using indexed states for progress tracking.
    State format: (string, fret, note_index)
    """

    def __init__(self, riff_notes):
        self.mapper = NoteMapper()
        self.cost_calculator = ErgonomicCost()
        self.riff_notes = riff_notes

        # Initial state: Using index -1 to represent the start before the first note
        initial_state = (0, 0, -1)
        super().__init__(initial_state)

    def actions(self, state):
        """
        Returns possible positions for the NEXT note in the sequence.
        """
        string, fret, note_index = state
        next_index = note_index + 1

        if next_index >= len(self.riff_notes):
            return []

        next_note = self.riff_notes[next_index]
        midi_val = self.mapper.note_to_midi(next_note)
        all_possible_next_pos = self.mapper.find_positions_on_fretboard(midi_val)

        # CSP Pruning:
        # If it's the first note (note_index == -1), all positions are valid.
        # Otherwise, check physical possibility from the current position.
        if note_index == -1:
            return [(s, f, next_index) for s, f in all_possible_next_pos]

        valid_actions = []
        for s_next, f_next in all_possible_next_pos:
            if self.cost_calculator.is_physically_possible((string, fret), (s_next, f_next)):
                valid_actions.append((s_next, f_next, next_index))

        return valid_actions

    def result(self, state, action):
        """
        The action itself is the next state (string, fret, next_index).
        """
        return action

    def goal_test(self, state):
        """
        Goal is reached when the note_index matches the last note of the riff.
        """
        return state[2] == len(self.riff_notes) - 1

    def path_cost(self, c, state1, action, state2):
        """
        Calculates g(n) using the ergonomic cost between coordinates.
        """
        # If moving from the starting dummy state, cost is 0
        if state1[2] == -1:
            return 0

        # Extract coordinates only for cost calculation
        pos1 = (state1[0], state1[1])
        pos2 = (state2[0], state2[1])

        return c + self.cost_calculator.calculate_step_cost(pos1, pos2)

    def h(self, node):
        """
        Admissible Heuristic: Number of notes remaining to be played.
        """
        return len(self.riff_notes) - 1 - node.state[2]