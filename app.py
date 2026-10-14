import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE = Path(__file__).parent
st.set_page_config(page_title="India Risk Intelligence", page_icon="🌐", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1400px;}
div[data-testid="stMetric"] {background: #f4f7fb; border: 1px solid #dce5ef; padding: 14px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("India Risk Intelligence")
st.caption("GEOPOLITICS / SECURITY / GEOECONOMICS")
st.write("An independent portfolio prototype tracking selected geopolitical risks affecting India's strategic and economic exposure.")
st.warning("Prototype notice: event rows are illustrative prompts, not verified event reports. Verify all data and sources before public use.")

@st.cache_data
def load_csv(filename):
    return pd.read_csv(BASE / "data" / filename)

scores = load_csv("risk_scores.csv")
events = load_csv("events.csv")

dashboard, tracker, briefs, method = st.tabs(["Risk Dashboard", "Event Tracker", "Intelligence Briefs", "Methodology"])

with dashboard:
    st.subheader("Selected India-facing risk categories")
    c1, c2, c3 = st.columns(3)
    c1.metric("Risk categories", len(scores))
    c2.metric("High-rated categories", int((scores["risk_level"].str.lower() == "high").sum()))
    c3.metric("Tracked indicators", "Framework-dependent")
    fig = px.bar(scores.sort_values("score"), x="score", y="risk_name", color="risk_level",
                 orientation="h", hover_data=["risk_id", "assessment_note"],
                 labels={"score":"Analyst score (illustrative)", "risk_name":"", "risk_level":"Assessment band"},
                 title="Illustrative risk assessment")
    fig.update_layout(height=380, margin=dict(l=5, r=5, t=55, b=5), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Scores are illustrative framework values, not probabilities or verified current risk measurements.")
    st.dataframe(scores[["risk_id","risk_name","score","risk_level","updated_at"]], use_container_width=True, hide_index=True)

with tracker:
    st.subheader("Event and development tracker")
    st.caption("Starter rows are illustrative monitoring prompts. Replace them with verified, dated events before public use.")
    f1, f2, f3 = st.columns([1,1,2])
    country = f1.selectbox("Geography", ["All"] + sorted(events["country"].dropna().unique().tolist()))
    category = f2.selectbox("Category", ["All"] + sorted(events["category"].dropna().unique().tolist()))
    query = f3.text_input("Search headline or India implication")
    filtered = events.copy()
    if country != "All":
        filtered = filtered[filtered["country"] == country]
    if category != "All":
        filtered = filtered[filtered["category"] == category]
    if query:
        mask = filtered["headline"].fillna("").str.contains(query, case=False) | filtered["india_implication"].fillna("").str.contains(query, case=False)
        filtered = filtered[mask]
    st.dataframe(filtered[["event_date","country","category","headline","source_name","source_url","record_status"]],
                 use_container_width=True, hide_index=True,
                 column_config={"source_url": st.column_config.LinkColumn("Source")})
    st.caption(f"{len(filtered)} record(s) shown.")

with briefs:
    st.subheader("Featured intelligence brief")
    st.markdown("### How West Asia instability can transmit risk to South Asia")
    st.markdown("""
**Key judgement**  
Disruption in West Asia can affect India through several connected channels. The scale of impact depends on duration, energy prices, shipping conditions, and market and policy responses.

**Transmission channels**
- **Energy:** higher crude prices can raise import costs and pressure fuel prices and the external balance.
- **Trade and shipping:** route disruption, insurance costs or longer voyages can increase freight costs and delivery uncertainty.
- **Remittances and migration:** instability can affect workers, employers and remittance flows; impacts vary by country and duration.
- **Inflation and markets:** energy and freight costs can feed into prices and business expectations.

**Indicators to monitor**
1. Brent crude price and volatility.
2. Shipping advisories and vessel-routing changes.
3. Freight and war-risk insurance costs, where reliable data is available.
4. Official statements and policy measures affecting energy supply.
5. Relevant trade, inflation and remittance releases.

**Analytical caveat**  
These are transmission mechanisms, not a claim that every channel is currently experiencing disruption. Attach dated evidence to each claim and distinguish observed developments from scenarios.
""")
    st.info("Replace this starter brief with your own researched version and add inline citations to primary and high-quality secondary sources.")

with method:
    st.subheader("Methodology and limitations")
    st.markdown("""
- **Risk score:** a framework-specific analyst judgement, not a probability.
- **Risk band:** a label attached to an example score. Define thresholds and apply them consistently.
- **Event record:** a structured monitoring item. Public release requires a dated event and a checked source.
- **India implication:** an analytical interpretation, not necessarily a confirmed outcome.
- **Confidence:** should reflect source quality, corroboration and uncertainty.
""")
    st.markdown("### Minimum publication standards")
    st.markdown("""
1. Prefer primary or authoritative sources.
2. Record the event date separately from the date the source was checked.
3. Separate facts, attributed claims, analyst judgement and scenarios.
4. Disclose missing data, stale indicators and scoring limitations.
5. Never claim real-time monitoring unless updates are actually performed.
""")
    st.write("Project purpose: demonstrate structured geopolitical monitoring, source-conscious analysis, data presentation and communication about India's external risk exposure.")
