import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.kpi_engine import compute_kpis
from src.forecasting import forecast_with_accuracy
from src.risk_engine import compute_risk
from src.decision_engine import generate_decisions
from src.ollama_interface import ask_ollama

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="AutoSCM AI", layout="wide")

# -----------------------------
# Clean UI Styling
# -----------------------------
st.markdown("""
<style>
.dataframe th {
    font-size: 14px;
    text-align: center;
}
.dataframe td {
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AutoSCM AI")
st.subheader("AI-Powered Supply Chain Decision System")

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.title("⚙️ Controls")

# Upload Section
st.sidebar.markdown("### 📂 Upload Your Data")

demand_file = st.sidebar.file_uploader("Upload Demand CSV", type=["csv"])
inventory_file = st.sidebar.file_uploader("Upload Inventory CSV", type=["csv"])
supplier_file = st.sidebar.file_uploader("Upload Supplier CSV", type=["csv"])

# Decision Mode
mode = st.sidebar.selectbox(
    "Decision Mode",
    ["Balanced", "Service Priority", "Cost Priority"]
)

run_button = st.sidebar.button("Run Full Analysis")
ai_button = st.sidebar.button("Generate AI Insights")

# -----------------------------
# Load Data
# -----------------------------
if demand_file and inventory_file and supplier_file:
    demand = pd.read_csv(demand_file)
    inventory = pd.read_csv(inventory_file)
    suppliers = pd.read_csv(supplier_file)
    st.sidebar.success("Custom data loaded ✅")
else:
    demand, inventory, suppliers = load_data()

# -----------------------------
# Run Analysis
# -----------------------------
if run_button:

    # KPIs
    kpis = compute_kpis(demand, inventory)

    # Forecast + Accuracy
    accuracy_df, forecast = forecast_with_accuracy(demand)

    kpis = kpis.merge(accuracy_df, on="sku", how="left")
    kpis = kpis.merge(forecast, on="sku", how="left")

    # Risk
    risk_df = compute_risk(kpis)

    # Decisions
    final_df = generate_decisions(risk_df, mode)

    st.success("✅ Analysis Complete")

    # -----------------------------
    # Add Risk Flag (better UX)
    # -----------------------------
    final_df["risk_flag"] = final_df["risk_level"].map({
        "HIGH": "🔴 HIGH",
        "MEDIUM": "🟡 MEDIUM",
        "LOW": "🟢 LOW"
    })

    # -----------------------------
    # Metrics
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Days of Cover", round(final_df["days_of_cover"].mean(), 2))
    col2.metric("High Risk SKUs", (final_df["risk_level"] == "HIGH").sum())
    col3.metric("Avg Demand CV", round(final_df["demand_cv"].mean(), 2))
    col4.metric("Avg WAPE", round(final_df["WAPE"].mean(), 2))

    # -----------------------------
    # Clean Table (NO ugly colors)
    # -----------------------------
    st.markdown("### 📊 Decision Intelligence Table")

    display_cols = [
        "sku",
        "on_hand",
        "reorder_point",
        "days_of_cover",
        "demand_cv",
        "WAPE",
        "risk_flag",
        "recommended_action"
    ]

    st.dataframe(
        final_df[display_cols],
        use_container_width=True
    )

    # -----------------------------
    # Top 10 Risk SKUs
    # -----------------------------
    st.markdown("### 🔥 Top 10 Risky SKUs")

    top_10 = final_df.sort_values(by="risk_score", ascending=False).head(10)

    st.dataframe(
        top_10[display_cols],
        use_container_width=True
    )

    # Save for AI
    st.session_state["final_df"] = final_df

# -----------------------------
# AI Insights
# -----------------------------
if ai_button:
    if "final_df" not in st.session_state:
        st.warning("⚠️ Run analysis first!")
    else:
        final_df = st.session_state["final_df"]

        st.markdown("### 🤖 AI Supply Chain Insights")

        prompt = f"""
        You are a senior supply chain planner.

        Analyze the dataset and:
        1. Identify top risks
        2. Explain WHY they are risky
        3. Suggest business actions
        4. Mention demand or inventory patterns

        Keep it concise and professional.

        Data:
        {final_df.to_string(index=False)}
        """

        with st.spinner("Analyzing..."):
            result = ask_ollama(prompt)

        # -----------------------------
        # Fallback if Ollama not available
        # -----------------------------
        if not result:

            st.info("⚠️ Running fallback AI (cloud mode)")

            high_risk = final_df[final_df["risk_level"] == "HIGH"]
            medium_risk = final_df[final_df["risk_level"] == "MEDIUM"]

            summary = f"""
            🔴 High Risk SKUs: {len(high_risk)}
            🟡 Medium Risk SKUs: {len(medium_risk)}

            Key Observations:
            - Inventory levels {'are critical' if len(high_risk) > 0 else 'are stable'}
            - Demand variability average: {round(final_df['demand_cv'].mean(), 2)}
            - Forecast accuracy (WAPE): {round(final_df['WAPE'].mean(), 2)}

            Recommendations:
            - Focus on high-risk SKUs for immediate action
            - Adjust reorder points for volatile demand
            - Improve forecasting for better planning
            """

            st.write(summary)

        else:
            st.write(result)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built by Rutwik Satish | AutoSCM AI")
