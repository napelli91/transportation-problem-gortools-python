import logging
from datetime import datetime
from typing import Tuple

from ortools.linear_solver import pywraplp

from src.utils import generate_data


class TransportationProblemSolver:
    def __init__(
        self,
        storages_nbr: int,
        stores_nbr: int,
        products_nbr: int,
        method="GLOP",
        seed=123,
    ) -> None:

        self.seed = seed

        self.solver = pywraplp.Solver.CreateSolver(method)
        self.solver_variables = {}
        self.solver_constraints = []
        self.solver_coefficients = []
        self.solved = False
        if not self.solver:
            raise "An error ocurred while loading solver"

        self.products_nbr = products_nbr
        self.stores_nbr = stores_nbr
        self.storages_nbr = storages_nbr

        self.costs = None
        self.stock = None
        self.demand = None

        logging.basicConfig(
            filename=f'output_data/solver_{datetime.now().strftime("%m%d%Y_%H%M")}.log',
            level=logging.INFO,
        )

    def _add_constraints(self):
        # [[START constraints]]
        # [[
        #   For every product and every store we can send up to the number
        #   of products in stock for a given storage
        # ]]
        for product in range(self.products_nbr):
            for storage in range(self.storages_nbr):
                self.solver.Add(
                    self.solver.Sum(
                        [
                            self.solver_variables[product, storage, store]
                            for store in range(self.stores_nbr)
                        ]
                    )
                    <= self.stock.loc[product, storage].values[0]
                )

        # [[
        #   For every product in every store is possible to send
        #   up to the number of demanded products for a given storage
        # ]]
        for product in range(self.products_nbr):
            for store in range(self.stores_nbr):
                self.solver.Add(
                    self.solver.Sum(
                        [
                            self.solver_variables[product, storage, store]
                            for storage in range(self.storages_nbr)
                        ]
                    )
                    <= self.demand.loc[product, store].values[0]
                )

        # [[
        #   Every store has to fulfill their demand
        # ]]
        for product in range(self.products_nbr):
            for store in range(self.stores_nbr):
                self.solver.Add(
                    self.solver.Sum(
                        [
                            self.solver_variables[product, storage, store]
                            for storage in range(self.storages_nbr)
                        ]
                    )
                    >= self.demand.loc[product, store].values[0]
                )
        # [[END constraints]]

    def _load_coefficients(self):
        self.solver.Minimize(
            self.solver.Sum(
                [
                    row.cost
                    * self.solver_variables[
                        int(row.var_name[0]), int(row.var_name[1]), int(row.var_name[2])
                    ]
                    for _, row in self.costs.iterrows()
                ]
            )
        )

    def _load_variables(self):
        for name in self.costs.var_name:
            product = int(name[0])
            storage = int(name[1])
            store = int(name[2])
            self.solver_variables[product, storage, store] = self.solver.IntVar(
                0, 999, name=f"x_{product}{storage}{store}"
            )

    def load_problem(self) -> None:
        logging.debug("Generating data for the problem...")
        self.costs, self.stock, self.demand = generate_data(
            self.products_nbr,
            self.stores_nbr,
            self.storages_nbr,
            seed=self.seed,
            save_data=False,
        )

        logging.debug("Loading Variables and constraints... ")
        self._load_variables()
        self._add_constraints()

        logging.debug("Setting the objective function... ")
        self._load_coefficients()

        logging.debug("Problem loaded correctly...")
        logging.debug(f"\tNumber of variables: {self.solver.NumVariables()}")
        logging.debug(f"\tNumber of constraints: {self.solver.NumConstraints()}")

    def get_result_objective(self) -> float:
        return self.solver.Objective().Value()

    def get_result_variables(self) -> dict:
        return {var: var.solution_value() for var in self.solver.variables()}

    def get_variable_result(self, product: int, local: int, deposit: int) -> float:
        return self.solver_variables[product, local, deposit].solution_value()

    def get_analytics(self) -> Tuple[int, int]:
        return self.solver.wall_time(), self.solver.iterations()

    def print_analytics(self) -> None:
        return f"""Solver usage analytics:
            Problem solved in {self.solver.wall_time()} milliseconds
            Problem solved in {self.solver.iterations()} iterations
        """

    def print_solution(self) -> None:
        if self.solved:
            logging.info("Solution:")
            logging.info("Objective value =", self.solver.Objective().Value())
            logging.info(self.solver_variables)
            for d in range(self.storages_nbr):
                logging.info(f"Deposit {d}")
                logging.info(20 * "-")
                for l in range(self.stores_nbr):
                    logging.info(f"\tLocal {l}")
                    logging.info("\t" + 20 * "-")
                    for p in range(self.products_nbr):
                        logging.info(
                            f"\t\tProduct {p}",
                            self.solver_variables[p, d, l].solution_value(),
                        )
        else:
            logging.info("Solver has not converged to a solution!!")

    def run_solver(self) -> None:
        status = self.solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            self.solved = True
