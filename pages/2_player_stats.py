# pages/2_player_stats.py
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from src.data_loader import load_lifetime, load_deliveries, load_matches
from src.features import combined_player_profile
import pandas as pd

st.title("👤 Player Statistics")

lifetime = load_lifetime()
players = sorted(lifetime['player'].unique())

player = st.selectbox("Select Player", players)

profile = combined_player_profile(player)

# Lifetime panel
st.subheader("🎖 Lifetime (aggregated IPL) stats")
if profile['lifetime'] is not None:
    life = profile['lifetime']
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Career Runs", life.get('total_runs', 0))
    with col2: st.metric("Career Avg", round(life.get('batting_average', 0) or 0, 2))
    with col3: st.metric("Career SR", round(life.get('strike_rate', 0) or 0, 2))
    with col4: st.metric("Wickets", life.get('wickets', 0))
else:
    st.info("Lifetime row not found for this player in cricket_full_ipl_lifetime.csv")

# IPL panel
st.subheader("📊 IPL (from deliveries)")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("IPL Runs", profile["runs"])
with col2: st.metric("Balls", profile["balls"])
with col3: st.metric("4s", profile["fours"])
with col4: st.metric("6s", profile["sixes"])

# Season trend
if not profile["season_runs"].empty:
    st.subheader("📈 Season-wise IPL Runs")
    fig, ax = plt.subplots()
    sns.lineplot(data=profile["season_runs"], x='season', y='batsman_runs', marker='o', ax=ax)
    ax.set_xlabel("Season")
    ax.set_ylabel("Runs")
    st.pyplot(fig)
else:
    st.info("No season-wise data available for this player.")
