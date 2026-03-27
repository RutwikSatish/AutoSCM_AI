import pandas as pd

def load_data():
    demand = pd.read_csv("data/demand.csv")
    inventory = pd.read_csv("data/inventory.csv")
    suppliers = pd.read_csv("data/suppliers.csv")

    demand["date"] = pd.to_datetime(demand["date"])
    return demand, inventory, suppliers
