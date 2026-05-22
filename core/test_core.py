import json
import tempfile
from pathlib import Path

import numpy as np

from core.data_loader import (
    build_distance_matrix,
    generate_random_cities,
    load_distance_matrix,
    load_from_json,
    load_from_txt,
)
from core.utils import build_result, calculate_total_distance, is_valid_path


def test_build_distance_matrix():
    coords = [(0, 0), (3, 4), (6, 0)]
    matrix = build_distance_matrix(coords)
    assert matrix.shape == (3, 3)
    assert np.isclose(matrix[0, 1], 5.0)
    assert np.isclose(matrix[1, 2], 5.0)


def test_calculate_total_distance_and_path():
    matrix = np.array([[0.0, 1.0], [1.0, 0.0]])
    path = [0, 1]
    assert is_valid_path(path, 2)
    assert calculate_total_distance(path, matrix) == 2.0


def test_invalid_paths():
    assert not is_valid_path([0, 0], 2)
    assert not is_valid_path([0], 2)
    assert not is_valid_path([0, 2], 2)


def test_json_loader():
    payload = {"coords": [[0, 0], [0, 3], [4, 0]]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
        tmp.write(json.dumps(payload))
        tmp_path = tmp.name

    matrix = load_from_json(tmp_path)
    Path(tmp_path).unlink()

    assert matrix.shape == (3, 3)
    assert np.isclose(matrix[0, 1], 3.0)
    assert np.isclose(matrix[0, 2], 4.0)


def test_txt_loader_coordinates():
    content = "3\n0 0\n0 3\n4 0\n"
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    matrix = load_from_txt(tmp_path)
    Path(tmp_path).unlink()

    assert matrix.shape == (3, 3)
    assert np.isclose(matrix[1, 2], 5.0)


def test_result_builder():
    result = build_result([0, 1], 10.0, 0.12)
    assert result["path"] == [0, 1]
    assert result["cost"] == 10.0
    assert result["time"] == 0.12


def test_generate_random_cities():
    matrix = generate_random_cities(5, seed=123)
    assert matrix.shape == (5, 5)
    assert np.allclose(np.diag(matrix), 0.0)


def test_load_distance_matrix_dispatch():
    content = "2\n0 0\n0 1\n"
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    matrix = load_distance_matrix(tmp_path)
    Path(tmp_path).unlink()
    assert matrix.shape == (2, 2)


if __name__ == "__main__":
    test_build_distance_matrix()
    test_calculate_total_distance_and_path()
    test_invalid_paths()
    test_json_loader()
    test_txt_loader_coordinates()
    test_result_builder()
    test_generate_random_cities()
    test_load_distance_matrix_dispatch()
    print("All core tests passed.")
