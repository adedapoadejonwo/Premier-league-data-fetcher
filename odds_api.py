import os
import requests
from db import get_conn
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

def fetch_odds():
    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={API_KEY}&regions=uk"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

def load_odds():
    data = fetch_odds()
    with get_conn() as conn:
        cur = conn.cursor()
        for game in data:
            match_id = game["id"]
            for bookmaker in game["bookmakers"]:
                for market in bookmaker["markets"]:
                    if market["key"] == "h2h":
                        odds = market["outcomes"]
                        home, draw, away = [o["price"] for o in odds]
                        cur.execute("""
                            INSERT INTO markets.odds_snapshot (match_id, captured_ts, book, home_win, draw, away_win)
                            VALUES (%s, NOW(), %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING;
                        """, (match_id, bookmaker["title"], home, draw, away))
        conn.commit()
    print("✅ Odds data updated.")
