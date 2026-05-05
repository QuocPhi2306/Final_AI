def calculate_total_distance(path, distance_matrix):
    if not path:
        return 0.0

    total = 0.0
    for i in range(len(path) - 1):
        total += distance_matrix[path[i]][path[i + 1]]

    if path[0] != path[-1]:
        total += distance_matrix[path[-1]][path[0]]

    return float(total)


def is_valid_path(path, n):
    if not isinstance(path, (list, tuple)):
        return False

    if len(path) != n:
        return False

    if any(not isinstance(city, int) for city in path):
        return False

    if any(city < 0 or city >= n for city in path):
        return False

    return len(set(path)) == n


def build_result(path, cost, elapsed_time):
    return {
        "path": list(path),
        "cost": float(cost),
        "time": float(elapsed_time),
    }
