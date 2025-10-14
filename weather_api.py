import os
import requests
from db import get_conn
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_weather(city):
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
    res.raise_for_status()
    return res.json()

def load_weather(match_id, city):
    data = fetch_weather(city)
    temp = data["main"]["temp"]
    rain = data.get("rain", {}).get("1h", 0)
    wind = data["wind"]["speed"]
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO match.weather (match_id, temp_c, wind_mps, rain_mm, category, provider)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (match_id) DO UPDATE
            SET temp_c = EXCLUDED.temp_c, wind_mps = EXCLUDED.wind_mps, rain_mm = EXCLUDED.rain_mm;
        """, (match_id, temp, wind, rain, 'clear', 'OpenWeather'))
        conn.commit()
    print(f"✅ Weather added for {city}")
