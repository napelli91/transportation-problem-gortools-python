import time
from pathlib import Path
from typing import Tuple

import pandas as pd
from numpy import random


def generate_data(
    number_of_products: int,
    number_of_stores: int,
    number_of_storages: int,
    seed: int = 123,
    save_data: bool = False,
) -> Tuple[pd.DataFrame]:
    """
    Generate random cost, stock, and demand data for a transportation problem.

    Args:
        number_of_products: How many distinct products to include.
        number_of_stores: How many stores (destinations) to include.
        number_of_storages: How many storage locations (origins) to include.
        seed: Seed for the random generator to keep results reproducible.
        save_data: When true, persist the generated demand dataframe to CSV in
            `input_data` with a timestamped filename.

    Returns:
        A tuple of three dataframes:
            - costs: columns `var_name` (product, storage, store) and `cost`.
            - stock: indexed by (product, storage) with a `stock` column.
            - demand: indexed by (product, store) with a `demand` column.
    """

    random.seed(seed)
    # Build vectors for store (store), deposits (storage), and products (products)

    products = list(range(number_of_products))
    stores = list(range(number_of_stores))
    storages = list(range(number_of_storages))

    # Build the distribution cost structure

    costs = []
    var_name = []

    for storage in storages:
        for store in stores:
            for product in products:
                var_name.append((product, storage, store))
                costs.append(random.normal(50, 5))

    # Build the cost DataFrame
    df_costs = pd.DataFrame(data={"var_name": var_name, "cost": costs})

    # Define the amount of stock for each deposit

    stock = []
    dep_s = []
    pro_s = []

    for storage in storages:
        for product in products:
            stock.append(random.randint(150, 350))
            dep_s.append(storage)
            pro_s.append(product)

    # Build the stock DataFrame

    df_stock = pd.DataFrame(data={"product": pro_s, "storage": dep_s, "stock": stock})

    df_stock.set_index(["product", "storage"], inplace=True)

    # Define the demand for each store

    demand = []
    loc_d = []
    pro_d = []

    for store in stores:
        for product in products:
            demand.append(random.randint(50, 250))
            loc_d.append(store)
            pro_d.append(product)

    # Build the demand DataFrame

    df_demand = pd.DataFrame(data={"product": pro_d, "store": loc_d, "demand": demand})
    df_demand.set_index(["product", "store"], inplace=True)

    if save_data:
        demand_path = Path("input_data") / f"demand_{int(time.time())}.csv"
        df_demand.to_csv(demand_path)

    return df_costs, df_stock, df_demand
