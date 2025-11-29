import logging
import json
from datetime import datetime

import numpy as np
from tqdm import tqdm

from src.transportation_problem_solver import TransportationProblemSolver

if __name__ == "__main__":
    storages = [5, 10]#, 15, 25, 50, 100, 150, 200]
    stores = [3, 5]# 10, 20, 50, 100, 150, 200]
    products = [3] * len(storages)

    n_exp = 1e2

    results = {}

    logging.basicConfig(
            filename=f'output_data/solver_{datetime.now().strftime("%m%d%Y_%H%M")}.log',
            level=logging.DEBUG,
        )

    for test_set in tqdm(range(len(storages)), desc="Running experiment... "):
        wall_time = []
        for _ in tqdm(range(int(n_exp)), desc="Experiment iteration"):
            problem = TransportationProblemSolver(
                storages_nbr=storages[test_set],
                stores_nbr=stores[test_set],
                products_nbr=products[test_set],
                method="CP_SAT",
                seed=123,
            )
            problem.load_problem()

            problem.run_solver()

            time, _ = problem.get_analytics()
            wall_time.append(time)
        results[test_set] = {"times": wall_time, "mean_time": np.mean(wall_time)}

        with open(
            f"./output_data/results_{datetime.now().strftime('%m%d%Y_%H%M')}.json", "w"
        ) as fh:
            json.dump(results, fh, indent=4)
