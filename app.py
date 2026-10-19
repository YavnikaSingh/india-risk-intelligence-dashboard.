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
