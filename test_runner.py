import numpy as np

from services.runner import run_algorithm
from core.utils import is_valid_path


def test_runner_backtracking():
    matrix = np.array(
        [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]]
    )
    result = run_algorithm("backtracking", matrix)

    assert is_valid_path(result["path"], 3)
    assert result["cost"] == 3.0
    assert result["time"] >= 0.0


def test_runner_bat_algorithm_default_params():
    matrix = np.array(
        [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]]
    )
    result = run_algorithm("ba", matrix)

    assert is_valid_path(result["path"], 3)
    assert result["cost"] == 3.0
    assert "convergence" in result
    assert isinstance(result["convergence"], list)


def test_runner_bat_algorithm_override_params():
    matrix = np.array(
        [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]]
    )
    result = run_algorithm("bat_algorithm", matrix, {"num_bats": 10, "max_iter": 10})

    assert is_valid_path(result["path"], 3)
    assert result["cost"] == 3.0


if __name__ == "__main__":
    test_runner_backtracking()
    test_runner_bat_algorithm_default_params()
    test_runner_bat_algorithm_override_params()
    print("Runner integration tests passed.")
