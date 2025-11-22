import pandas as pd
from src.data_loader import load_lifetime, load_deliveries, load_matches


def combined_player_profile(player):
    lifetime = load_lifetime()
    deliveries = load_deliveries()

    # Clean column names
    lifetime.columns = [c.strip() for c in lifetime.columns]
    deliveries.columns = [c.strip() for c in deliveries.columns]

    # lifetime stats (batting + bowling)
    life_row = lifetime[lifetime["Player"] == player]

    if life_row.empty:
        return None

    out = {}

    # Batting
    out["Total Runs"] = float(life_row["total_runs"].values[0])
    out["Average"] = float(life_row["average"].values[0])
    out["Strike Rate"] = float(life_row["strike_rate"].values[0])

    # IPL batting
    out["IPL Runs"] = float(life_row["ipl_runs"].values[0])
    out["IPL 4s"] = float(life_row["fours"].values[0])
    out["IPL 6s"] = float(life_row["sixes"].values[0])

    # Bowling
    out["IPL Wickets"] = float(life_row["wickets"].values[0])
    out["Economy Rate"] = float(life_row["economy"].values[0])
    out["Bowling Average"] = float(life_row["bowling_average"].values[0])
    out["Bowling Strike Rate"] = float(life_row["bowling_strike_rate"].values[0])

    return out
