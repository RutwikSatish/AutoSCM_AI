def forecast_with_accuracy(demand):
    df = demand.copy()

    forecast = (
        df.groupby("sku")["demand"]
        .mean()
        .reset_index(name="forecast")
    )

    df = df.merge(forecast, on="sku")

    df["abs_error"] = abs(df["demand"] - df["forecast"])
    df["bias"] = df["demand"] - df["forecast"]

    accuracy = df.groupby("sku").agg({
        "abs_error": "mean",
        "demand": "mean",
        "bias": "mean"
    }).reset_index()

    accuracy["WAPE"] = accuracy["abs_error"] / accuracy["demand"]

    return accuracy[["sku", "WAPE", "bias"]], forecast