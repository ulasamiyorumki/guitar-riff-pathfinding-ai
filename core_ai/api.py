from core_ai.search_astar import astar_search, GuitarPathProblem
from core_ai.cost import ErgonomicCost
import pandas as pd
import random

def run_fingering_algorithm(riff):
    """
    Runs the A* fingering optimization and returns the final path + analysis.
    """
    if not riff:
        return [], {"total": 0}

    problem = GuitarPathProblem(riff)
    evaluator = problem.cost_calculator  # SAME cost model as A*

    path_nodes = astar_search(problem)

    if not path_nodes:
        return [], {"total": 0}

    final_path = [
        (node.state[0], node.state[1])
        for node in path_nodes
        if node.state[2] != -1
    ]

    analysis = calculate_final_metrics(final_path, evaluator)

    return final_path, analysis


def calculate_final_metrics(path, evaluator: ErgonomicCost):
    """
    Produces metrics CONSISTENT with the A* cost function.
    """

    total_cost = 0.0
    stretch_total = 0.0
    string_total = 0.0
    penalty_count = 0
    open_string_count = 0

    for i in range(1, len(path)):
        p1, p2 = path[i - 1], path[i]

        step_cost = evaluator.calculate_step_cost(p1, p2)
        total_cost += step_cost

        stretch = abs(p1[1] - p2[1]) * evaluator.FRET_STRETCH_WEIGHT
        string = abs(p1[0] - p2[0]) * evaluator.STRING_CHANGE_WEIGHT

        stretch_total += stretch
        string_total += string

        if not evaluator.is_physically_possible(p1, p2):
            penalty_count += 1

        if p2[1] == 0 and evaluator.is_physically_possible(p1, p2):
            open_string_count += 1

    return {
        "stretch": round(stretch_total, 2),
        "string": round(string_total, 2),
        "pos": round(stretch_total + string_total, 2),
        "penalty_count": penalty_count,
        "total": round(total_cost, 2)
    }

def generate_random_riff_from_excel():
    """
    Selects 10 random notes from column B (rows 2-48) of guitar_midi_notes.xlsx.
    """
    try:
        # Load the Excel file focusing on the specific range
        df = pd.read_excel("guitar_midi_notes.xlsx", usecols=[1], skiprows=1, nrows=47, header=None,engine="openpyxl")

        # Convert the column data to a list and filter out empty values
        all_notes = df.iloc[:, 0].dropna().tolist()

        # Pick 10 random samples from the list
        selected_notes = random.sample(all_notes, 10)

        return " ".join(map(str, selected_notes))
    except Exception as e:
        print(f"Excel Reading Error: {e}")
        # Fallback riff in case of file issues
        return "E2 G2 B2 D3 G3 B3 E4 D4 B3 G3"