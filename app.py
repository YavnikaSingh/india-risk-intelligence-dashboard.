import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE = Path(__file__).parent

st.set_page_config(
    page_title="India Risk Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
:root {
    --navy: #0b1628;
    --blue: #4b83c3;
    --ink: #17263b;
    --muted: #68778b;
    --line: #dce4ed;
    --canvas: #0a1220;
}
.stApp { background: var(--canvas); color: var(--ink); }
.block-container { max-width: 1450px; padding-top: 1.3rem; padding-bottom: 3rem; }
[data-testid="stHeader"] { background: rgba(243,246,250,.92); }
h1, h2, h3 { color: var(--navy); letter-spacing: -.025em; }
h1 { font-size: clamp(2rem, 3vw, 2.8rem) !important; font-weight: 750 !important; }
h2 { font-size: 1.45rem !important; font-weight: 700 !important; }
h3 { font-size: 1.08rem !important; font-weight: 700 !important; }
p, li, label { color: #35465c; }
.hero {
    background: linear-gradient(115deg, #101d32 0%, #193555 72%, #244b70 100%);
    border: 1px solid #203a5b; border-radius: 18px;
    padding: 1.7rem 1.8rem 1.5rem; margin: .2rem 0 1.1rem;
    color: #f7faff; box-shadow: 0 8px 22px rgba(16,29,50,.10);
}
.hero-kicker { color: #a9c6e7; font-size: .72rem; font-weight: 750; letter-spacing: .17em; text-transform: uppercase; margin-bottom: .65rem; }
.hero-title { color: #fff; font-size: clamp(1.85rem, 3.2vw, 2.65rem); font-weight: 780; letter-spacing: -.035em; line-height: 1.12; margin-bottom: .55rem; }
.hero-copy { color: #d7e3f1; max-width: 850px; font-size: 1rem; line-height: 1.6; margin-bottom: 0; }
.hero-meta { color: #a9c6e7; font-size: .75rem; font-weight: 650; letter-spacing: .07em; margin-top: 1.15rem; text-transform: uppercase; }
.section-eyebrow { color: var(--muted); font-size: .73rem; font-weight: 750; letter-spacing: .13em; text-transform: uppercase; margin-bottom: .2rem; }
.section-intro { color: var(--muted); font-size: .92rem; margin-top: -.25rem; margin-bottom: 1rem; }
div[data-testid="stMetric"] { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 1rem 1.1rem; box-shadow: 0 3px 12px rgba(22,42,67,.035); }
div[data-testid="stMetricLabel"] { color: var(--muted); font-size: .83rem; font-weight: 650; }
div[data-testid="stMetricValue"] { color: var(--navy); font-size: 1.9rem; font-weight: 760; }
div[data-testid="stTabs"] button { font-weight: 650; padding-top: .8rem; padding-bottom: .8rem; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #245c91; }
div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
div[data-testid="stAlert"] { border-radius: 12px; }
.note-card { background: #fff; border: 1px solid var(--line); border-left: 4px solid var(--blue); border-radius: 10px; padding: .9rem 1rem; margin: .6rem 0 1rem; color: #43536a; font-size: .9rem; line-height: 1.55; }
.footer { color: #718096; border-top: 1px solid var(--line); padding-top: 1rem; margin-top: 2rem; font-size: .8rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="hero-kicker">Independent geopolitical research · Portfolio prototype</div>
  <div class="hero-title">India Risk Intelligence</div>
  <p class="hero-copy">
    A structured view of selected geopolitical, security and geoeconomic risks
    that may affect India's strategic and economic exposure.
  </p>
  <div class="hero-meta">Geopolitics&nbsp;&nbsp; / &nbsp;&nbsp;Security&nbsp;&nbsp; / &nbsp;&nbsp;Geoeconomics</div>
</div>
""", unsafe_allow_html=True)

st.warning(
    "Prototype notice: event rows are illustrative monitoring prompts, not verified event reports. "
    "Verify dates, claims and sources before treating any entry as a current development."
)

@st.cache_data
def load_csv(filename):
    return pd.read_csv(BASE / filename)

scores = load_csv("risk_scores.csv")
events = load_csv("events.csv")

if "risk_level" in scores.columns:
    scores["risk_level"] = scores["risk_level"].fillna("Unclassified").astype(str)
if "country" in events.columns:
    events["country"] = events["country"].fillna("Unspecified").astype(str)
if "category" in events.columns:
    events["category"] = events["category"].fillna("Unclassified").astype(str)

dashboard, tracker, briefs, method = st.tabs(
    ["Risk Dashboard", "Event Tracker", "Intelligence Briefs", "Methodology"]
)

with dashboard:
    st.markdown('<div class="section-eyebrow">Overview</div>', unsafe_allow_html=True)
    st.subheader("Selected India-facing risk categories")
    st.markdown(
        '<div class="section-intro">Framework-based assessments for portfolio demonstration — not live risk measurements.</div>',
        unsafe_allow_html=True,
    )
    high_count = int((scores["risk_level"].str.lower() == "high").sum()) if "risk_level" in scores.columns else 0
    c1, c2, c3 = st.columns(3)
    c1.metric("Risk categories", len(scores))
    c2.metric("High-rated categories", high_count)
    c3.metric("Tracked indicators", "Framework-based")

    chart_col, guide_col = st.columns([2.2, 1], gap="large")
    with chart_col:
        st.markdown("### Relative assessment by category")
        fig = px.bar(
            scores.sort_values("score"),
            x="score",
            y="risk_name",
            color="risk_level",
            orientation="h",
            hover_data=[c for c in ["risk_id", "assessment_note", "updated_at"] if c in scores.columns],
            labels={"score": "Illustrative analyst score", "risk_name": "", "risk_level": "Assessment band"},
            color_discrete_map={
                "Low": "#5C9B8B", "Moderate": "#D4A64D", "High": "#C96861",
                "Critical": "#8E3B4A", "Unclassified": "#8290A3",
            },
        )
        fig.update_layout(
            height=410, margin=dict(l=5, r=12, t=15, b=5),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Arial, sans-serif", color="#35465c", size=12),
            legend_title_text="",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            xaxis=dict(showgrid=True, gridcolor="#e3e9f0", zeroline=False),
            yaxis=dict(showgrid=False, automargin=True), bargap=.32,
        )
        st.plotly_chart(fig, use_container_width=True)
    with guide_col:
        st.markdown("### How to read this")
        st.markdown("""
        <div class="note-card"><strong>Score</strong><br>A framework-specific analyst judgement. It is not a probability or forecast.</div>
        <div class="note-card"><strong>Assessment band</strong><br>A label attached to the example score. Thresholds should be defined and applied consistently.</div>
        <div class="note-card"><strong>Publication standard</strong><br>Attach dated evidence to claims and distinguish observed facts from scenarios and analyst interpretation.</div>
        """, unsafe_allow_html=True)

    st.markdown("### Risk register")
    display_cols = [c for c in ["risk_id", "risk_name", "score", "risk_level", "updated_at"] if c in scores.columns]
    st.dataframe(
        scores[display_cols], use_container_width=True, hide_index=True,
        column_config={
            "risk_id": st.column_config.TextColumn("ID"),
            "risk_name": st.column_config.TextColumn("Risk category", width="large"),
            "score": st.column_config.NumberColumn("Score", format="%.2f"),
            "risk_level": st.column_config.TextColumn("Assessment band"),
            "updated_at": st.column_config.TextColumn("Last updated"),
        },
    )
    st.caption("Scores are illustrative framework values, not probabilities or verified current risk measurements.")

with tracker:
    st.markdown('<div class="section-eyebrow">Monitoring workspace</div>', unsafe_allow_html=True)
    st.subheader("Event and development tracker")
    st.markdown(
        '<div class="section-intro">Filter structured monitoring records. Confirm each event and source before publication.</div>',
        unsafe_allow_html=True,
    )
    st.info("Starter rows are illustrative monitoring prompts. They should not be presented as verified event reports until checked.")

    f1, f2, f3 = st.columns([1, 1, 2])
    country_options = ["All"] + sorted(events["country"].dropna().unique().tolist()) if "country" in events.columns else ["All"]
    category_options = ["All"] + sorted(events["category"].dropna().unique().tolist()) if "category" in events.columns else ["All"]
    country = f1.selectbox("Geography", country_options)
    category = f2.selectbox("Category", category_options)
    query = f3.text_input("Search headline or India implication", placeholder="e.g. energy, shipping, trade")

    filtered = events.copy()
    if country != "All" and "country" in filtered.columns:
        filtered = filtered[filtered["country"] == country]
    if category != "All" and "category" in filtered.columns:
        filtered = filtered[filtered["category"] == category]
    if query:
        searchable_cols = [c for c in ["headline", "india_implication", "country", "category"] if c in filtered.columns]
        if searchable_cols:
            mask = pd.Series(False, index=filtered.index)
            for col in searchable_cols:
                mask = mask | filtered[col].fillna("").astype(str).str.contains(query, case=False, regex=False)
            filtered = filtered[mask]

    event_cols = [c for c in ["event_date", "country", "category", "headline", "source_name", "source_url", "record_status"] if c in filtered.columns]
    st.dataframe(
        filtered[event_cols], use_container_width=True, hide_index=True,
        column_config={
            "event_date": st.column_config.TextColumn("Event date"),
            "country": st.column_config.TextColumn("Geography"),
            "category": st.column_config.TextColumn("Category"),
            "headline": st.column_config.TextColumn("Development / monitoring prompt", width="large"),
            "source_name": st.column_config.TextColumn("Source"),
            "source_url": st.column_config.LinkColumn("Open source", display_text="View source"),
            "record_status": st.column_config.TextColumn("Record status"),
        },
    )
    st.caption(f"{len(filtered)} record(s) shown.")

with briefs:
    st.markdown('<div class="section-eyebrow">Analytical output</div>', unsafe_allow_html=True)
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
    st.info("This is a starter brief. Before publishing it as analysis, add inline citations, dates and a clear distinction between evidence and judgement.")

with method:
    st.markdown('<div class="section-eyebrow">Transparency</div>', unsafe_allow_html=True)
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
    st.markdown(
        '<div class="note-card"><strong>Project purpose</strong><br>'
        'Demonstrate structured geopolitical monitoring, source-conscious analysis, data presentation and communication about India’s external risk exposure.</div>',
        unsafe_allow_html=True,
    )

st.markdown("""
<div class="footer">
  INDIA RISK INTELLIGENCE · Independent portfolio prototype · Framework-based analysis, not an operational alert service
</div>
""", unsafe_allow_html=True)
