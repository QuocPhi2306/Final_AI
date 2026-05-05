def run_algorithm(algo_name, distance_matrix, params=None):
    if algo_name == "backtracking":
        from algorithims.backtracking import solve_tsp_backtracking
        return solve_tsp_backtracking(distance_matrix)

    elif algo_name in ("ba", "bat", "bat_algorithm"):
        from algorithims.bat_algorithm import solve_tsp_ba
        return solve_tsp_ba(distance_matrix, params or {})

    else:
        raise ValueError("Unknown algorithm")
