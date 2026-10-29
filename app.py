import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="India Risk Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE = Path(__file__).parent


# -----------------------------
# DARK DASHBOARD DESIGN
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: #0a1220;
    color: #e5edf7;
}
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4 {
    color: #edf5ff !important;
}
p, label, li {
    color: #b7c6d9;
}
[data-testid="stHeader"] {
    background: transparent;
}
[data-testid="stMetric"] {
    background: #111f33;
    border: 1px solid #2a3b53;
    border-radius: 14px;
    padding: 18px;
}
[data-testid="stMetricLabel"] {
    color: #9aabc2 !important;
}
[data-testid="stMetricValue"] {
    color: #f1f7ff !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #2dd4bf !important;
    border-bottom-color: #2dd4bf !important;
}
.event-card {
    background: #111f33;
    border: 1px solid #2a3b53;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
    min-height: 210px;
}
.eyebrow {
    color: #6ee7d2;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.hero {
    background: linear-gradient(120deg, #12233b, #193d5c);
    border: 1px solid #294968;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 24px;
}
hr {
    border-color: #26384f;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# LOAD EXISTING DATA
# -----------------------------
def load_csv(filename):
    path = BASE / filename
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path).fillna("")
    except Exception:
        return pd.DataFrame()


events = load_csv("events.csv")
risks = load_csv("risk_scores.csv")


def find_column(df, candidates):
    for column in df.columns:
        if str(column).strip().lower() in candidates:
            return column
    return None


# Identify common event columns
headline_col = find_column(
    events, {"headline", "title", "event", "event_title", "description"}
)
country_col = find_column(
    events, {"country", "geography", "location", "region"}
)
category_col = find_column(
    events, {"category", "event_type", "topic", "sector"}
)
severity_col = find_column(
    events, {"severity", "risk_level", "level", "impact"}
)
date_col = find_column(
    events, {"event_date", "date", "published_date"}
)
source_col = find_column(
    events, {"source_name", "source", "publisher"}
)
url_col = find_column(
    events, {"source_url", "url", "link"}
)


# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">Independent geopolitical monitoring</div>
    <h1 style="margin-top:12px;">India Risk Intelligence</h1>
    <p style="font-size:17px;">
        Monitoring geopolitical developments, strategic risks and
        their potential implications for India.
    </p>
    <p style="font-size:12px; color:#9bb5d2;">
        RISK MONITORING &nbsp; / &nbsp; EVENT TRACKER
        &nbsp; / &nbsp; STRATEGIC ANALYSIS
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# SUMMARY METRICS
# -----------------------------
if severity_col and not events.empty:
    severity_values = events[severity_col].astype(str).str.lower()
    high_count = severity_values.isin(
        ["high", "critical", "severe"]
    ).sum()
    medium_count = severity_values.isin(
        ["medium", "moderate"]
    ).sum()
    low_count = severity_values.isin(
        ["low", "minor"]
    ).sum()
else:
    high_count = medium_count = low_count = 0

m1, m2, m3, m4 = st.columns(4)

m1.metric("Events monitored", len(events))
m2.metric("High / critical", int(high_count))
m3.metric("Medium / moderate", int(medium_count))
m4.metric("Risk areas", len(risks))

st.markdown("---")


# -----------------------------
# MAIN TABS
# -----------------------------
tracker, register, brief, methodology = st.tabs([
    "Event Tracker",
    "Risk Register",
    "Intelligence Brief",
    "Methodology",
])


# -----------------------------
# EVENT TRACKER
# -----------------------------
with tracker:
    st.markdown('<div class="eyebrow">Situational awareness</div>',
                unsafe_allow_html=True)
    st.header("Monitored Developments")
    st.caption(
        "Search and filter the recorded events. Verify original sources "
        "before relying on any entry."
    )

    if events.empty:
        st.warning(
            "No event records were loaded. Check that events.csv exists "
            "in the same GitHub folder as app.py."
        )
    else:
        f1, f2, f3 = st.columns([2, 1, 1])

        with f1:
            search_term = st.text_input(
                "Search events",
                placeholder="Search headlines, countries or keywords..."
            )

        with f2:
            if country_col:
                countries = sorted({
                    str(v) for v in events[country_col]
                    if str(v).strip()
                })
                selected_country = st.selectbox(
                    "Geography", ["All"] + countries
                )
            else:
                selected_country = "All"

        with f3:
            if severity_col:
                severities = sorted({
                    str(v) for v in events[severity_col]
                    if str(v).strip()
                })
                selected_severity = st.selectbox(
                    "Severity", ["All"] + severities
                )
            else:
                selected_severity = "All"

        filtered = events.copy()

        if search_term:
            mask = filtered.astype(str).apply(
                lambda col: col.str.contains(
                    search_term, case=False, na=False
                )
            ).any(axis=1)
            filtered = filtered[mask]

        if country_col and selected_country != "All":
            filtered = filtered[
                filtered[country_col].astype(str) == selected_country
            ]

        if severity_col and selected_severity != "All":
            filtered = filtered[
                filtered[severity_col].astype(str) == selected_severity
            ]

        st.caption(f"{len(filtered)} events match your filters.")

        if filtered.empty:
            st.info("No matching events. Try changing your filters.")
        else:
            for start in range(0, len(filtered), 3):
                cols = st.columns(3)

                for col, (_, event) in zip(
                    cols, filtered.iloc[start:start + 3].iterrows()
                ):
                    headline = (
                        str(event[headline_col])
                        if headline_col else "Event headline unavailable"
                    )
                    country = (
                        str(event[country_col])
                        if country_col else "Geography unspecified"
                    )
                    category = (
                        str(event[category_col])
                        if category_col else "Uncategorised"
                    )
                    severity = (
                        str(event[severity_col])
                        if severity_col else "Unclassified"
                    )
                    event_date = (
                        str(event[date_col])
                        if date_col else "Date not provided"
                    )
                    source = (
                        str(event[source_col])
                        if source_col else "Source not listed"
                    )
                    url = str(event[url_col]) if url_col else ""

                    severity_lower = severity.lower()
                    if severity_lower in {"critical", "high", "severe"}:
                        accent = "#fb7185"
                    elif severity_lower in {"medium", "moderate"}:
                        accent = "#fbbf24"
                    elif severity_lower in {"low", "minor"}:
                        accent = "#34d399"
                    else:
                        accent = "#60a5fa"

                    with col:
                        st.markdown(
                            f"""
                            <div class="event-card"
                                 style="border-top:3px solid {accent};">
                                <div style="color:{accent};
                                     font-size:11px;font-weight:700;
                                     letter-spacing:1px;">
                                    {severity.upper()}
                                </div>
                                <h3 style="margin-top:12px;">
                                    {headline}
                                </h3>
                                <p>{country} · {event_date}</p>
                                <p>Category: {category}</p>
                                <p style="font-size:12px;">
                                    Source: {source}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        if url.startswith(("https://", "http://")):
                            st.link_button(
                                "Open source",
                                url,
                                use_container_width=True
                            )

        with st.expander("View complete event data"):
            st.dataframe(filtered, use_container_width=True, hide_index=True)


# -----------------------------
# RISK REGISTER
# -----------------------------
with register:
    st.markdown('<div class="eyebrow">Strategic exposure</div>',
                unsafe_allow_html=True)
    st.header("Risk Register")
    st.caption(
        "Review the available risk scores and indicators from your dataset."
    )

    if risks.empty:
        st.warning(
            "No risk scores were loaded. Check that risk_scores.csv exists "
            "in the same GitHub folder as app.py."
        )
    else:
        st.metric("Risk records", len(risks))
        st.dataframe(
            risks,
            use_container_width=True,
            hide_index=True
        )

        with st.expander("Inspect risk data columns"):
            st.write(list(risks.columns))


# -----------------------------
# INTELLIGENCE BRIEF
# -----------------------------
with brief:
    st.markdown('<div class="eyebrow">Analytical output</div>',
                unsafe_allow_html=True)
    st.header("Featured Intelligence Brief")
    st.subheader(
        "How West Asia instability can transmit risk to South Asia"
    )

    st.markdown("""
    **Key judgement**

    Instability in West Asia can affect India through interconnected
    energy, shipping, trade and economic channels. The scale of impact
    depends on the duration of disruption and the responses of markets
    and governments.

    **Transmission channels**

    - **Energy:** Changes in crude oil prices can affect import costs
      and India's external balance.
    - **Trade and shipping:** Route disruptions can increase freight
      costs and delivery uncertainty.
    - **Remittances:** Prolonged instability may affect workers and
      remittance flows in exposed countries.
    - **Inflation:** Higher energy and transport costs can contribute
      to price pressures.

    **Indicators to monitor**

    1. Brent crude prices and volatility.
    2. Shipping advisories and route changes.
    3. Freight and insurance costs, where reliable data is available.
    4. Official energy supply announcements.
    5. Relevant trade and inflation releases.

    **Analytical caveat**

    These are possible transmission mechanisms, not confirmation that
    every channel is currently disrupted. Add dated evidence and
    distinguish observed developments from scenarios before publishing.
    """)


# -----------------------------
# METHODOLOGY
# -----------------------------
with methodology:
    st.markdown('<div class="eyebrow">Transparency</div>',
                unsafe_allow_html=True)
    st.header("Methodology and Limitations")

    st.markdown("""
    - **Risk score:** an analytical assessment under the project's
      chosen framework, not a statistical probability.
    - **Risk band:** a category assigned using defined score thresholds.
    - **Event record:** a monitored item that should have a date and
      a source that has been checked.
    - **India implication:** an analytical interpretation, not
      necessarily a confirmed outcome.
    - **Confidence:** should reflect source quality, corroboration
      and uncertainty.

    ### Publication standards

    1. Prefer primary and authoritative sources.
    2. Record event dates and source publication dates accurately.
    3. Separate facts, attributed claims and analytical judgement.
    4. Disclose missing data and scoring limitations.
    5. Do not claim real-time monitoring unless updates are actually
       performed.
    """)

    st.info(
        "This dashboard is an independent portfolio prototype, not an "
        "operational alert service. Verify events and sources before use."
    )


# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption(
    "INDIA RISK INTELLIGENCE  ·  Independent portfolio project  ·  "
    "Framework-based analysis"
)
