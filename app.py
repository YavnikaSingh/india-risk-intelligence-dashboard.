                    with st.container(border=True):
                        st.markdown(
                            f"""
                            <div style="height:4px;
                                background:{severity_color};
                                border-radius:4px;
                                margin-bottom:12px;"></div>
                            <div style="font-size:11px;
                                color:{severity_color};
                                font-weight:700;
                                text-transform:uppercase;
                                letter-spacing:1px;">
                                {severity_label} SEVERITY
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.markdown(f"**{headline}**")
                        st.caption(f"{country_name} · {event_date}")

                        st.markdown(
                            f"""
                            <div style="font-size:12px;
                                color:#94a3b8;
                                margin:8px 0;">
                                {category_name}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.caption(f"Status: {status}")
                        st.caption(f"Source: {source_name}")

                        if source_url.startswith(("https://", "http://")):
                            st.markdown(f"[Open source]({source_url})")

    st.caption(
        "Portfolio prototype. Verify event dates, claims and sources "
        "before treating entries as confirmed current developments."
    )

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
