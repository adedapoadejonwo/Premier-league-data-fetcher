import requests
import pandas as pd
from db import get_conn
import logging
import time

BASE_URL = "https://fantasy.premierleague.com/api"

def fetch_bootstrap_static():
    """Fetch FPL bootstrap static data with error handling"""
    try:
        res = requests.get(f"{BASE_URL}/bootstrap-static/", timeout=30)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch FPL data: {e}")
        raise

def load_players(data):
    """Load player data into database with error handling"""
    try:
        df = pd.DataFrame(data["elements"])
        df_players = df[[
            "id", "web_name", "team", "now_cost", "form", "total_points", "minutes", "selected_by_percent"
        ]]

        with get_conn() as conn:
            cur = conn.cursor()
            for _, row in df_players.iterrows():
                try:
                    cur.execute("""
                        INSERT INTO player.person (player_id, full_name, known_as, primary_pos, created_at)
                        VALUES (%s, %s, %s, %s, NOW())
                        ON CONFLICT (player_id) DO NOTHING;
                    """, (row.id, row.web_name, row.web_name, None))
                except Exception as e:
                    logging.warning(f"Failed to insert player {row.web_name}: {e}")
                    continue
            conn.commit()
    except Exception as e:
        logging.error(f"Failed to load players: {e}")
        raise

def run_fpl_ingestion():
    """Run FPL data ingestion with error handling"""
    try:
        data = fetch_bootstrap_static()
        load_players(data)
        print("✅ FPL players updated.")
    except Exception as e:
        logging.error(f"FPL ingestion failed: {e}")
        raise
