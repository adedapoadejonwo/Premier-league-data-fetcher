import os
import requests
from db import get_conn
from dotenv import load_dotenv
import logging
import time

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

def fetch_odds():
    """Fetch odds data with error handling"""
    if not API_KEY:
        raise ValueError("ODDS_API_KEY environment variable is not set")
    
    try:
        url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={API_KEY}&regions=uk"
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch odds data: {e}")
        raise

def load_odds():
    """Load odds data into database with error handling"""
    try:
        data = fetch_odds()
        with get_conn() as conn:
            cur = conn.cursor()
            for game in data:
                try:
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
                except Exception as e:
                    logging.warning(f"Failed to process game {game.get('id', 'unknown')}: {e}")
                    continue
            conn.commit()
        print("✅ Odds data updated.")
    except Exception as e:
        logging.error(f"Failed to load odds: {e}")
        raise
