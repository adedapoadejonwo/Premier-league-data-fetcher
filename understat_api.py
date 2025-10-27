import requests
import pandas as pd
from db import get_conn
import logging
import re

def fetch_team_xg(team_name):
    """Fetch team xG data with error handling"""
    try:
        url = f"https://understat.com/team/{team_name}/2024"
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        text = res.text
        
        # Parse JSON inside HTML with better error handling
        start_pattern = r"var\s+shotsData\s*=\s*JSON\.parse\('"
        match = re.search(start_pattern, text)
        if not match:
            raise ValueError(f"Could not find shots data for team {team_name}")
        
        start = match.end()
        end = text.find("')", start)
        if end == -1:
            raise ValueError(f"Could not parse shots data for team {team_name}")
            
        json_str = text[start:end].encode('utf8').decode('unicode_escape')
        return pd.read_json(json_str)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch Understat data for {team_name}: {e}")
        raise
    except Exception as e:
        logging.error(f"Failed to parse Understat data for {team_name}: {e}")
        raise

def load_team_strength(team_name):
    """Load team strength data with error handling"""
    try:
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
    except Exception as e:
        logging.error(f"Failed to load team strength for {team_name}: {e}")
        raise
