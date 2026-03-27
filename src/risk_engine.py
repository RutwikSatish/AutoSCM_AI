def compute_risk(df):
    scores = []

    for _, row in df.iterrows():
        score = 0

        # -----------------------------
        # 1. Inventory Risk (Most Critical)
        # -----------------------------
        if row["days_of_cover"] < row["lead_time_days"]:
            score += 5  # strong penalty

        # -----------------------------
        # 2. Demand Variability Risk
        # -----------------------------
        if row["demand_cv"] > 0.5:
            score += 3
        elif row["demand_cv"] > 0.3:
            score += 2

        # -----------------------------
        # 3. Reorder Risk
        # -----------------------------
        if row["reorder_gap"] < 0:
            score += 4

        # -----------------------------
        # 4. Forecast Accuracy Risk
        # -----------------------------
        if "WAPE" in row:
            if row["WAPE"] > 0.4:
                score += 3
            elif row["WAPE"] > 0.2:
                score += 2

        scores.append(score)

    df["risk_score"] = scores

    # -----------------------------
    # Risk Classification (balanced distribution)
    # -----------------------------
    def classify(score):
        if score >= 8:
            return "HIGH"
        elif score >= 4:
            return "MEDIUM"
        else:
            return "LOW"

    df["risk_level"] = df["risk_score"].apply(classify)

    return df
