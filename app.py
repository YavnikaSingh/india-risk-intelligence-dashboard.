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

/* Dark intelligence dashboard refresh */
.stApp {
    background: #0a1220;
    color: #e5edf7;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #edf5ff !important;
}

p, li, label, [data-testid="stCaptionContainer"] {
    color: #b7c6d9;
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

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #2dd4bf !important;
    border-bottom-color: #2dd4bf !important;
