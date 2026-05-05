import json
import os
import numpy as np


def load_from_txt(file_path):
    with open(file_path, "r") as f:
        lines = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]

    if not lines:
        raise ValueError(f"No valid data found in {file_path}")

    rows = [line.split() for line in lines]

    if len(rows[0]) == 1 and len(rows) == int(rows[0][0]) + 1:
        n = int(rows[0][0])
        body = rows[1:]
        if all(len(r) == 2 for r in body):
            coords = np.array(body, dtype=float)
            return build_distance_matrix(coords)
        if all(len(r) == n for r in body):
            return np.array(body, dtype=float)

    if all(len(r) == 2 for r in rows):
        coords = np.array(rows, dtype=float)
        return build_distance_matrix(coords)

    if all(len(r) == len(rows) for r in rows):
        return np.array(rows, dtype=float)

    raise ValueError("TXT file must contain coordinates or a square distance matrix.")


def load_from_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    if isinstance(data, dict):
        if "distance_matrix" in data:
            return np.array(data["distance_matrix"], dtype=float)
        if "coords" in data:
            coords = np.array(data["coords"], dtype=float)
            return build_distance_matrix(coords)
        if "cities" in data:
            coords = np.array(data["cities"], dtype=float)
            return build_distance_matrix(coords)

        raise ValueError(
            "JSON file must contain 'distance_matrix', 'coords', or 'cities'."
        )

    arr = np.array(data, dtype=float)

    if arr.ndim == 2 and arr.shape[1] == 2:
        return build_distance_matrix(arr)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        return arr

    raise ValueError("JSON file must contain coordinates or a square distance matrix.")


def load_distance_matrix(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return load_from_txt(file_path)
    if ext == ".json":
        return load_from_json(file_path)
    raise ValueError("Unsupported file format. Use .txt or .json")


def generate_random_cities(n, seed=42):
    np.random.seed(seed)
    coords = np.random.rand(n, 2) * 100
    return build_distance_matrix(coords)


def build_distance_matrix(coords):
    coords = np.asarray(coords, dtype=float)
    if coords.ndim != 2 or coords.shape[1] != 2:
        raise ValueError("Coordinates must be a list or array of pairs [x, y].")

    n = coords.shape[0]
    matrix = np.zeros((n, n), dtype=float)

    for i in range(n):
        for j in range(n):
            matrix[i, j] = np.linalg.norm(coords[i] - coords[j])

    return matrix
