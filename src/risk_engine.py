def compute_risk(df):
    scores = []

    for _, row in df.iterrows():
        score = 0

        if row["days_of_cover"] < row["lead_time_days"]:
            score += 3

        if row["demand_cv"] > 0.5:
            score += 2

        if row["reorder_gap"] < 0:
            score += 3

        if row.get("WAPE", 0) > 0.3:
            score += 2

        scores.append(score)

    df["risk_score"] = scores

    df["risk_level"] = df["risk_score"].apply(
        lambda x: "HIGH" if x >= 6 else "MEDIUM" if x >= 3 else "LOW"
    )

    return df
