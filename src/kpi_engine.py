import pandas as pd
import numpy as np

def compute_kpis(demand, inventory):
    stats = demand.groupby("sku")["demand"].agg(["mean", "std"]).reset_index()
    stats.columns = ["sku", "avg_demand", "std_demand"]

    df = inventory.merge(stats, on="sku", how="left")

    df["days_of_cover"] = df["on_hand"] / df["avg_demand"]
    df["demand_cv"] = df["std_demand"] / df["avg_demand"]

    service_level = 1.65
    df["safety_stock"] = service_level * df["std_demand"] * np.sqrt(df["lead_time_days"])

    df["reorder_gap"] = df["on_hand"] - df["reorder_point"]

    return df