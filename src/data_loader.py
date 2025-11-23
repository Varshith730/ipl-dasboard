# src/data_loader.py
import pandas as pd
import zipfile
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # project root

@lru_cache(maxsize=1)
def load_matches(path:str = str(ROOT / "data" / "matches.csv")):
    """
    Load matches.csv (small CSV)
    """
    df = pd.read_csv(path)
    # normalize column names
    df.columns = [c.strip() for c in df.columns]
    return df

@lru_cache(maxsize=1)
def load_deliveries(zip_path: str = str(ROOT / "data" / "deliveries.csv.zip"),
                    inner_name: str = "deliveries.csv"):
    """
    Load deliveries.csv from inside deliveries.csv.zip without extracting.
    """
    with zipfile.ZipFile(zip_path, "r") as z:
        with z.open(inner_name) as f:
            df = pd.read_csv(f)
    df.columns = [c.strip() for c in df.columns]
    return df

@lru_cache(maxsize=1)
def load_lifetime(path:str = str(ROOT / "data" / "cricket_full_ipl_lifetime.csv")):
    """
    Load lifetime/player dataset (cricket_full_ipl_lifetime.csv).
    """
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    return df
