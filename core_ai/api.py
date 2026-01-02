from core_ai.search_astar import GuitarPathProblem, astar_search


def run_fingering_algorithm(riff_list):
    """
    Main API interface that bridges the GUI with the A* search logic.
    Input: List of note names, e.g., ['D4', 'E4', 'F4']
    Output: List of coordinates, e.g., [(3, 7), (3, 9), (3, 10)]
    """

    # 1. Create the problem instance (Load the riff into the system)
    problem = GuitarPathProblem(riff_list)

    # 2. Find the optimal solution using the A* engine
    # This function is imported from search_astar.py
    solution_path = astar_search(problem)

    # 3. Format the result for the GUI (List of tuples)
    formatted_result = []

    if solution_path:
        for node in solution_path:
            # Skip the START state (index -1) and take only real notes
            if node.state[2] != -1:
                string, fret, _ = node.state
                formatted_result.append((string, fret))

    return formatted_result

# Example Usage (For Testing):
# coords = run_fingering_algorithm(['G2', 'A#2', 'C3'])
# print(coords) -> [(6, 3), (6, 6), (5, 3)]