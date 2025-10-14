import requests
import pandas as pd
from db import get_conn

BASE_URL = "https://fantasy.premierleague.com/api"

def fetch_bootstrap_static():
    res = requests.get(f"{BASE_URL}/bootstrap-static/")
    res.raise_for_status()
    return res.json()

def load_players(data):
    df = pd.DataFrame(data["elements"])
    df_players = df[[
        "id", "web_name", "team", "now_cost", "form", "total_points", "minutes", "selected_by_percent"
    ]]

    with get_conn() as conn:
        cur = conn.cursor()
        for _, row in df_players.iterrows():
            cur.execute("""
                INSERT INTO player.person (player_id, full_name, known_as, primary_pos, created_at)
                VALUES (%s, %s, %s, %s, NOW())
                ON CONFLICT (player_id) DO NOTHING;
            """, (row.id, row.web_name, row.web_name, None))
        conn.commit()

def run_fpl_ingestion():
    data = fetch_bootstrap_static()
    load_players(data)
    print("✅ FPL players updated.")
