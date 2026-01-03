from core_ai.note_mapping import NoteMapper
from core_ai.cost import ErgonomicCost

mapper = NoteMapper(num_frets=22)
evaluator = ErgonomicCost()

def run_fingering_algorithm(riff):
    """
    Finds the globally optimal path for the entire riff using Dynamic Programming.
    """
    if not riff:
        return [], {"stretch": 0, "string": 0, "total": 0}

    # Step 1: Map notes to possible positions
    note_options = []
    for note_name in riff:
        midi_val = mapper.note_to_midi(note_name)
        if midi_val is None: continue
        options = mapper.find_positions_on_fretboard(midi_val)
        if options:
            note_options.append(options)

    if not note_options:
        return [], {"stretch": 0, "string": 0, "total": 0}

    # Step 2: Dynamic Programming (DP) Table
    dp = []
    first_step = {opt: (0, None) for opt in note_options[0]}
    dp.append(first_step)

    for i in range(1, len(note_options)):
        current_step_results = {}
        for current_opt in note_options[i]:
            best_prev_cost = float('inf')
            best_prev_node = None

            for prev_opt, (prev_total_cost, _) in dp[i - 1].items():
                # We use our new evaluator class here
                transition_cost = evaluator.calculate_step_cost(prev_opt, current_opt)
                total_cost_to_current = prev_total_cost + transition_cost

                if total_cost_to_current < best_prev_cost:
                    best_prev_cost = total_cost_to_current
                    best_prev_node = prev_opt

            current_step_results[current_opt] = (best_prev_cost, best_prev_node)
        dp.append(current_step_results)

    # Step 3: Backtrack to find the optimal path
    path = []
    last_step = dp[-1]
    current_node = min(last_step, key=lambda k: last_step[k][0])

    for i in range(len(dp) - 1, -1, -1):
        path.append(current_node)
        current_node = dp[i][current_node][1]

    path.reverse()

    # Step 4: Analytics
    analysis = {"stretch": 0.0, "string": 0.0, "total": dp[-1][path[-1]][0]}
    for i in range(1, len(path)):
        p1, p2 = path[i - 1], path[i]
        analysis["stretch"] += abs(p1[1] - p2[1]) * evaluator.FRET_STRETCH_WEIGHT
        analysis["string"] += abs(p1[0] - p2[0]) * evaluator.STRING_CHANGE_WEIGHT

    return path, analysis