import numpy as np

def load_from_txt(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    n = int(lines[0].strip())
    coords = []

    for line in lines[1:]:
        x, y = map(float, line.strip().split())
        coords.append((x, y))

    return build_distance_matrix(coords)


def generate_random_cities(n, seed=42):
    np.random.seed(seed)
    coords = np.random.rand(n, 2) * 100
    return build_distance_matrix(coords)


def build_distance_matrix(coords):
    n = len(coords)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            matrix[i][j] = np.linalg.norm(
                np.array(coords[i]) - np.array(coords[j])
            )

    return matrix