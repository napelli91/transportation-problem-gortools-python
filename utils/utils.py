import pandas as pd
from typing import Tuple
from numpy import random


def generate_data(number_of_products: int,
                  number_of_stores: int,
                  number_of_storages: int,
                  seed: int = 123) -> Tuple[pd.DataFrame]:

    random.seed(seed)
    # Armamos los vectores de store(store), Depósitos(storage) y products(products)

    products = list(range(number_of_products))
    store = list(range(number_of_stores))
    storage = list(range(number_of_storages))

    # Armamos la estructura de costos de distribución

    costs = []
    var_name = []

    for d in storage:
        for l in store:
            for n in products:
                var_name.append((n,d,l))
                costs.append(random.normal(50, 5))
    
    # Cosntruimos el DF de costos
    df_costs = pd.DataFrame(data={
        'var_name': var_name,
        'cost': costs})

    # Definimos la cantidad de stock de cada depósito

    stock = []
    dep_s = []
    pro_s = []

    for d in storage:
        for n in products:
            stock.append(random.randint(150, 350))
            dep_s.append(d)
            pro_s.append(n)

    # Cosntruimos el DF de Stocks

    df_stock = pd.DataFrame(data={
        'product': pro_s,
        'storage': dep_s,
        'stock': stock})

    df_stock.set_index(['product', 'storage'], inplace=True)

    # Definimos la demanda de cada local

    demand = []
    loc_d = []
    pro_d = []

    for l in store:
        for n in products:
            demand.append(random.randint(50, 250))
            loc_d.append(l)
            pro_d.append(n)

    # Cosntruimos el DF de demand

    df_demand = pd.DataFrame(data={
        'product': pro_d,
        'store': loc_d,
        'demand': demand})
    df_demand.set_index(['product', 'store'], inplace=True)

    return df_costs, df_stock, df_demand
