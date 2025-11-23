# pages/4_season_analysis.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.data_loader import load_deliveries, load_matches

st.title("📅 Season Analysis")

deliveries = load_deliveries()
matches = load_matches()

merged = deliveries.merge(matches[['id','season']], left_on='match_id', right_on='id', how='left')

season_list = sorted(merged['season'].dropna().unique())
season = st.selectbox("Select Season", season_list)

st.subheader("🏏 Top Run Scorers")
season_batting = merged[merged['season'] == season].groupby('batter')['batsman_runs'].sum().reset_index().sort_values('batsman_runs', ascending=False).head(10)
st.table(season_batting)

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(data=season_batting, x='batsman_runs', y='batter', ax=ax)
ax.set_title(f"Top runscorers - {season}")
st.pyplot(fig)

st.subheader("🎯 Top Wicket Takers")
# valid wicket kinds credited to bowler
invalid = ["run out", "retired hurt", "obstructing the field"]
valid_wickets = merged[(merged['is_wicket'] == 1) & (~merged['dismissal_kind'].isin(invalid))]
season_wickets = valid_wickets[valid_wickets['season'] == season].groupby('bowler').size().reset_index(name='wickets').sort_values('wickets', ascending=False).head(10)
st.table(season_wickets)

fig2, ax2 = plt.subplots(figsize=(8,5))
sns.barplot(data=season_wickets, x='wickets', y='bowler', ax=ax2)
ax2.set_title(f"Top wicket takers - {season}")
st.pyplot(fig2)
