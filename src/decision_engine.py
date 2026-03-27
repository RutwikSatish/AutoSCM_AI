def generate_decisions(df, mode="Balanced"):
    actions = []

    for _, row in df.iterrows():

        if mode == "Service Priority":
            if row["risk_level"] == "HIGH":
                action = "Aggressive replenishment + increase safety stock"
            else:
                action = "Maintain high service levels"

        elif mode == "Cost Priority":
            if row["risk_level"] == "HIGH":
                action = "Controlled reorder + avoid overstock"
            else:
                action = "Minimize holding cost"

        else:  # Balanced
            if row["risk_level"] == "HIGH":
                action = "Expedite + monitor supplier"
            elif row["risk_level"] == "MEDIUM":
                action = "Adjust reorder point"
            else:
                action = "No action needed"

        actions.append(action)

    df["recommended_action"] = actions
    return df