def calculate_total_distance(path, distance_matrix):
    total = 0
    n = len(path)

    for i in range(n - 1):
        total += distance_matrix[path[i]][path[i + 1]]

    # quay về điểm đầu
    total += distance_matrix[path[-1]][path[0]]

    return total


def is_valid_path(path, n):
    return len(path) == n and len(set(path)) == n