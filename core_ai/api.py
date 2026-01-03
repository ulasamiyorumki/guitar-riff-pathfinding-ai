import math
from core_ai.note_mapping import NoteMapper

# Initialize the guitar fretboard mapper
mapper = NoteMapper(num_frets=22)

# --- Ergonomic Cost Parameters ---
FRET_STRETCH_WEIGHT = 1.0  # Cost per horizontal fret distance
STRING_CHANGE_WEIGHT = 2.0  # Cost per vertical string jump
OPEN_STRING_BONUS = -0.5  # Reward for using open strings (easier to play)
MAX_REACHABLE_STRETCH = 4  # Maximum fret span for a static hand position


def calculate_cost(pos1, pos2):
    """
    Calculates the physical effort required to move from pos1 to pos2.
    Implements the core ergonomic logic.
    """
    if pos1 is None:
        return 0

    s1, f1 = pos1
    s2, f2 = pos2

    fret_diff = abs(f1 - f2)
    string_diff = abs(s1 - s2)

    # Base cost calculation
    cost = (fret_diff * FRET_STRETCH_WEIGHT) + (string_diff * STRING_CHANGE_WEIGHT)

    # Apply bonus for open strings (Fret 0)
    if f2 == 0:
        cost += OPEN_STRING_BONUS

    # Constraint Check: Apply penalty if the stretch exceeds the physical limit (4 frets)
    # This guides the algorithm to prefer hand shifts over impossible stretches.
    if f1 != 0 and f2 != 0 and fret_diff > MAX_REACHABLE_STRETCH:
        cost += 15.0

    return max(0.1, cost)


def run_fingering_algorithm(riff):
    """
    Finds the globally optimal path for the entire riff using Dynamic Programming.
    This ensures the most efficient finger positions across all notes.
    """
    if not riff:
        return [], {"stretch": 0, "string": 0, "total": 0}

    # Step 1: Map each note in the riff to all its possible fretboard positions
    note_options = []
    for note_name in riff:
        midi_val = mapper.note_to_midi(note_name)
        if midi_val is None:
            continue
        options = mapper.find_positions_on_fretboard(midi_val)
        if options:
            note_options.append(options)

    if not note_options:
        return [], {"stretch": 0, "string": 0, "total": 0}

    # Step 2: Dynamic Programming Table (Finding the minimum cost path)
    dp = []

    # Initialize the first note options with 0 starting cost
    first_step = {opt: (0, None) for opt in note_options[0]}
    dp.append(first_step)

    # Calculate cumulative costs for each subsequent note
    for i in range(1, len(note_options)):
        current_step_results = {}
        for current_opt in note_options[i]:
            best_prev_cost = float('inf')
            best_prev_node = None

            for prev_opt, (prev_total_cost, _) in dp[i - 1].items():
                transition_cost = calculate_cost(prev_opt, current_opt)
                total_cost_to_current = prev_total_cost + transition_cost

                if total_cost_to_current < best_prev_cost:
                    best_prev_cost = total_cost_to_current
                    best_prev_node = prev_opt

            current_step_results[current_opt] = (best_prev_cost, best_prev_node)
        dp.append(current_step_results)

    # Step 3: Backtrack to reconstruct the optimal path
    path = []
    last_step = dp[-1]
    # Pick the ending position with the lowest total accumulated cost
    current_node = min(last_step, key=lambda k: last_step[k][0])

    for i in range(len(dp) - 1, -1, -1):
        path.append(current_node)
        current_node = dp[i][current_node][1]

    path.reverse()

    # Step 4: Calculate Analytical Breakdown for the UI
    analysis = {"stretch": 0.0, "string": 0.0, "total": 0.0}
    for i in range(len(path)):
        if i == 0:
            continue

        p1, p2 = path[i - 1], path[i]
        f_diff = abs(p1[1] - p2[1])
        s_diff = abs(p1[0] - p2[0])

        analysis["stretch"] += (f_diff * FRET_STRETCH_WEIGHT)
        analysis["string"] += (s_diff * STRING_CHANGE_WEIGHT)

    # The final total cost includes bonuses and penalties tracked in DP
    analysis["total"] = dp[-1][path[-1]][0]

    return path, analysis