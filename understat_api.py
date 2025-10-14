import requests
import pandas as pd
from db import get_conn

def fetch_team_xg(team_name):
    url = f"https://understat.com/team/{team_name}/2024"
    text = requests.get(url).text
    # Parse JSON inside HTML
    start = text.find("('") + 2
    end = text.find("')")
    json_str = text[start:end].encode('utf8').decode('unicode_escape')
    return pd.read_json(json_str)

def load_team_strength(team_name):
    df = fetch_team_xg(team_name)
    avg_xg = df['xG'].mean()
    avg_xga = df['xGA'].mean()
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO features.team_strength (season_id, team_id, as_of_ts, att_rating, def_rating, half_life_gm, sample_n)
            VALUES (1, (SELECT team_id FROM core.team WHERE name=%s), NOW(), %s, %s, 0.9, %s)
        """, (team_name, avg_xg, avg_xga, len(df)))
        conn.commit()
    print(f"✅ Team {team_name} xG data loaded.")
