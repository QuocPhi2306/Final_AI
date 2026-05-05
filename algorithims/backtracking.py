import time
from core.utils import calculate_total_distance

def solve_tsp_backtracking(distance_matrix):
    n = len(distance_matrix)
    best_cost = float("inf")
    best_path = []

    def backtrack(path, visited, current_cost):
        nonlocal best_cost, best_path

        if len(path) == n:
            total_cost = current_cost + distance_matrix[path[-1]][path[0]]
            if total_cost < best_cost:
                best_cost = total_cost
                best_path = path[:]
            return

        if current_cost >= best_cost:
            return  # prune

        for i in range(n):
            if not visited[i]:
                visited[i] = True
                path.append(i)

                backtrack(
                    path,
                    visited,
                    current_cost + distance_matrix[path[-2]][i]
                )

                visited[i] = False
                path.pop()

    start_time = time.time()

    visited = [False] * n
    visited[0] = True

    backtrack([0], visited, 0)

    end_time = time.time()

    return {
        "path": best_path,
        "cost": best_cost,
        "time": end_time - start_time
    }