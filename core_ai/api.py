from core_ai.search_astar import GuitarPathProblem
from core_ai.models import Node
import heapq


def run_fingering_algorithm(riff_list):
    """
    Main API interface that bridges the GUI with the A* search logic.
    Input: List of note names ['A2', 'C3', 'E3']
    Output: List of coordinates [(string, fret), ...]
    """

    def astar_search(problem):
        node = Node(problem.initial)
        frontier = []
        heapq.heappush(frontier, (0 + problem.h(node), node))
        explored = set()

        while frontier:
            _, node = heapq.heappop(frontier)
            if problem.goal_test(node.state):
                return node.path()
            explored.add(node.state)
            for child in node.expand(problem):
                if child.state not in explored:
                    f_value = child.path_cost + problem.h(child)
                    heapq.heappush(frontier, (f_value, child))
        return None

    # 1. Create the problem instance
    problem = GuitarPathProblem(riff_list)

    # 2. Find the optimal solution
    solution_path = astar_search(problem)

    # 3. Format the result for the GUI
    formatted_result = []
    if solution_path:
        for node in solution_path:
            if node.state[2] != -1:  # Skip START state
                string, fret, _ = node.state
                formatted_result.append((string, fret))

    return formatted_result