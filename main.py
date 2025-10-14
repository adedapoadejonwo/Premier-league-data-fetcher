from fpl_api import run_fpl_ingestion
from understat_api import load_team_strength
from odds_api import load_odds
from weather_api import load_weather

def main():
    print("🏁 Starting FPL Data Collector...")
    run_fpl_ingestion()
    load_team_strength("Arsenal")
    load_odds()
    load_weather(1, "London")
    print("✅ All data fetched and loaded!")

if __name__ == "__main__":
    main()
