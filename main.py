from core.config import BA_PARAMS, DEFAULT_NUM_CITIES
from core.data_loader import generate_random_cities
from services.runner import run_algorithm

if __name__ == "__main__":
    matrix = generate_random_cities(DEFAULT_NUM_CITIES)

    result_bt = run_algorithm("backtracking", matrix)
    result_ba = run_algorithm("ba", matrix, BA_PARAMS)

    print("Backtracking:", result_bt)
    print("Bat Algorithm:", result_ba)
