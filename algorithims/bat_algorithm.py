import random
import time
import math
from core.utils import build_result, calculate_total_distance
 
 
def random_path(n):
    path = list(range(n))
    random.shuffle(path)
    return path
 
 
def swap(path):
    a, b = random.sample(range(len(path)), 2)
    path[a], path[b] = path[b], path[a]
    return path
 
 
def local_search(path):
    return swap(path[:])
 
 
def generate_swap_sequence(current, target):
    swaps = []
    temp = current[:]
    for i in range(len(temp)):
        if temp[i] != target[i]:
            j = temp.index(target[i])
            swaps.append((i, j))
            temp[i], temp[j] = temp[j], temp[i]
    return swaps
 
 
def apply_velocity(path, velocity):
    new_path = path[:]
    for i, j in velocity:
        new_path[i], new_path[j] = new_path[j], new_path[i]
    return new_path
 
 
def solve_tsp_ba(distance_matrix, params):
    n = len(distance_matrix)
    num_bats = params["num_bats"]
    max_iter = params["max_iter"]
    alpha = params["alpha"]
    gamma = params["gamma"]
 
    f_min = 0.0
    f_max = 2.0
 
    if num_bats <= 0 or max_iter <= 0:
        raise ValueError("Bat Algorithm requires positive num_bats and max_iter")
 
    # --- Khởi tạo đàn dơi ---
    bats = [random_path(n) for _ in range(num_bats)]
    fitness = [calculate_total_distance(p, distance_matrix) for p in bats]
    frequencies = [0.0 for _ in range(num_bats)]
    loudness = [1.0 for _ in range(num_bats)]
    pulse_rate = [0.5 for _ in range(num_bats)]
    history = []
 
    best_idx = fitness.index(min(fitness))
    best_path = bats[best_idx][:]
    best_cost = fitness[best_idx]
    history = [best_cost]

    start_time = time.time()
 
    for t in range(1, max_iter + 1):          # BUG FIX: dùng t thay _ để tính pulse_rate
        for i in range(num_bats):
 
            # --- Frequency update ---
            beta = random.random()
            frequencies[i] = f_min + (f_max - f_min) * beta
 
            # --- Velocity & position update (discrete TSP) ---
            velocity = generate_swap_sequence(bats[i], best_path)
            new_path = apply_velocity(bats[i], velocity)
 
            # --- Local search (khi pulse rate thấp → explore) ---
            # BUG FIX: new_path = local_search phải NẰM TRONG if block
            if random.random() > pulse_rate[i]:
                new_path = local_search(best_path)
 
            # --- Tính fitness nghiệm mới ---
            new_cost = calculate_total_distance(new_path, distance_matrix)
 
            # --- Acceptance condition ---
            if new_cost < fitness[i] and random.random() < loudness[i]:
                bats[i] = new_path
                fitness[i] = new_cost
 
                # Loudness giảm dần (dơi gần mồi → phát âm nhỏ hơn)
                loudness[i] *= alpha
 
                # Pulse rate tăng dần theo iteration
                pulse_rate[i] = 0.5 * (1 - math.exp(-gamma * t))
 
                # Cập nhật global best
                if new_cost < best_cost:
                    best_cost = new_cost
                    best_path = new_path[:]
                history.append(best_cost)

                end_time = time.time()

                result = build_result(
                       best_path,
                       best_cost,
                       end_time - start_time
                       )

                result["history"] = history

                return result
