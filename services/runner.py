from core.config import BA_PARAMS


def run_algorithm(algo_name, distance_matrix, params=None):

    algo_name = str(
        algo_name
    ).strip().lower()

    if algo_name == "backtracking":

        from algorithms.backtracking import (
            solve_tsp_backtracking
        )

        return solve_tsp_backtracking(
            distance_matrix
        )

    elif algo_name in (
        "ba",
        "bat",
        "bat_algorithm"
    ):

        from algorithms.bat_algorithm import (
            solve_tsp_ba
        )

        merged_params = {
            **BA_PARAMS,
            **(params or {})
        }

        return solve_tsp_ba(
            distance_matrix,
            merged_params
        )

    raise ValueError(
        f"Unknown algorithm '{algo_name}'. "
        "Supported values are "
        "'backtracking', "
        "'ba', "
        "'bat', "
        "'bat_algorithm'."
    )