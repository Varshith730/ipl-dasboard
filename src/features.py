# src/features.py
import pandas as pd
from rapidfuzz import process
from src.data_loader import load_lifetime, load_deliveries, load_matches

# threshold for fuzzy matching names
FUZZY_THRESHOLD = 70

def best_match(name, candidates):
    """Return best fuzzy match from candidates or None if score too low."""
    if name is None or len(str(name).strip()) == 0:
        return None
    match = process.extractOne(name, candidates)
    if match is None:
        return None
    matched_name, score, _ = match
    return matched_name if score >= FUZZY_THRESHOLD else None

def combined_player_profile(player_name):
    """
    Returns a dict with lifetime + IPL (deliveries) aggregated stats for a player.
    Lifetime CSV expected columns include:
      player, total_runs, batting_average, strike_rate, fours, sixes,
      wickets, economy, bowling_average, bowling_strike_rate
    """
    lifetime = load_lifetime()
    deliveries = load_deliveries()
    matches = load_matches()

    # normalize columns
    lifetime.columns = [c.strip() for c in lifetime.columns]
    deliveries.columns = [c.strip() for c in deliveries.columns]
    matches.columns = [c.strip() for c in matches.columns]

    # candidate name lists
    life_names = lifetime['player'].astype(str).unique().tolist()
    deliv_names = deliveries['batter'].astype(str).unique().tolist()

    # fuzzy match name to lifetime dataset and deliveries
    matched_life = best_match(player_name, life_names)
    matched_deliv = best_match(player_name, deliv_names)

    life_row = lifetime[lifetime['player'] == matched_life] if matched_life else pd.DataFrame()
    # Prepare output with defaults
    out = {
        "player": player_name,
        "lifetime": None,
        # IPL aggregates
        "runs": 0,
        "balls": 0,
        "fours": 0,
        "sixes": 0,
        "season_runs": pd.DataFrame(columns=['season', 'batsman_runs']),
        # bowling (from lifetime if exists)
        "wickets": 0,
        "economy": None,
        "bowling_average": None,
        "bowling_strike_rate": None
    }

    # lifetime stats fill
    if not life_row.empty:
        row = life_row.iloc[0]
        out["lifetime"] = row.to_dict()
        # fallback keys if different names: try common column names
        # prefer 'total_runs' else try 'total_runs' or other variants
        # we will not overwrite IPL aggregates here (those come from deliveries)
        out["wickets"] = int(row['wickets']) if 'wickets' in row and not pd.isna(row['wickets']) else out["wickets"]
        out["economy"] = float(row['economy']) if 'economy' in row and not pd.isna(row['economy']) else out["economy"]
        out["bowling_average"] = float(row['bowling_average']) if 'bowling_average' in row and not pd.isna(row['bowling_average']) else out["bowling_average"]
        out["bowling_strike_rate"] = float(row['bowling_strike_rate']) if 'bowling_strike_rate' in row and not pd.isna(row['bowling_strike_rate']) else out["bowling_strike_rate"]

    # deliveries (IPL) aggregates
    if matched_deliv:
        player_del = deliveries[deliveries['batter'] == matched_deliv]
        if not player_del.empty:
            out["runs"] = int(player_del['batsman_runs'].sum())
            out["balls"] = int(player_del.shape[0])
            out["fours"] = int((player_del['batsman_runs'] == 4).sum())
            out["sixes"] = int((player_del['batsman_runs'] == 6).sum())

            merged = player_del.merge(matches[['id', 'season']], left_on='match_id', right_on='id', how='left')
            season_runs = merged.groupby('season')['batsman_runs'].sum().reset_index()
            season_runs = season_runs.rename(columns={'batsman_runs': 'batsman_runs'})
            out["season_runs"] = season_runs

            # compute IPL wickets credited to bowler for this player? (not needed here)
            # But we can compute bowler-wickets statistics elsewhere
    return out
