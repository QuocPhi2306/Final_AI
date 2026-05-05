import random
import time
from core.utils import calculate_total_distance

def random_path(n):
    path = list(range(n))
    random.shuffle(path)
    return path


def swap(path):
    a, b = random.sample(range(len(path)), 2)
    path[a], path[b] = path[b], path[a]
    return path


def solve_tsp_ba(distance_matrix, params):
    n = len(distance_matrix)
    num_bats = params["num_bats"]
    max_iter = params["max_iter"]

    bats = [random_path(n) for _ in range(num_bats)]
    fitness = [calculate_total_distance(p, distance_matrix) for p in bats]

    best_idx = fitness.index(min(fitness))
    best_path = bats[best_idx][:]
    best_cost = fitness[best_idx]

    start_time = time.time()

    for _ in range(max_iter):
        for i in range(num_bats):
            new_path = swap(bats[i][:])
            new_cost = calculate_total_distance(new_path, distance_matrix)

            if new_cost < fitness[i]:
                bats[i] = new_path
                fitness[i] = new_cost

                if new_cost < best_cost:
                    best_cost = new_cost
                    best_path = new_path[:]

    end_time = time.time()

    return {
        "path": best_path,
        "cost": best_cost,
        "time": end_time - start_time
    }