import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.data_loader import generate_random_cities
from core.config import BA_PARAMS
from services.runner import run_algorithm
from visualization.plot_route import plot_route
from visualization.plot_convergence import plot_convergence


if __name__ == "__main__":
    coords, matrix = generate_random_cities(10, return_coords=True)

    result_ba = run_algorithm("ba", matrix, BA_PARAMS)

    print("Bat Algorithm result:")
    print("  cost:", result_ba["cost"])
    print("  time:", result_ba["time"])
    print("  history length:", len(result_ba.get("history", [])))
    print("  history first 5:", result_ba.get("history", [])[:5])
    print("  path:", result_ba["path"])

    plot_route(coords, result_ba["path"], title="Bat Algorithm TSP Route")
    plot_convergence(result_ba["history"], title="Bat Algorithm Convergence")
