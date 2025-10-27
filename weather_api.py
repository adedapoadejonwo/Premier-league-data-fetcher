import os
import requests
from db import get_conn
from dotenv import load_dotenv
import logging

load_dotenv()

API_KEY = os.getenv("WEATHERAPI_KEY")

def fetch_weather(city):
    """Fetch weather data from WeatherAPI.com with error handling"""
    if not API_KEY:
        raise ValueError("WEATHERAPI_KEY environment variable is not set")
    
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch weather data for {city}: {e}")
        raise

def load_weather(match_id, city):
    """Load weather data into database with error handling"""
    try:
        data = fetch_weather(city)
        current = data["current"]
        
        temp = current["temp_c"]
        wind = current["wind_kph"] / 3.6  # Convert km/h to m/s
        rain = current.get("precip_mm", 0)
        condition = current["condition"]["text"]
        
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO match.weather (match_id, temp_c, wind_mps, rain_mm, category, provider)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (match_id) DO UPDATE
                SET temp_c = EXCLUDED.temp_c, wind_mps = EXCLUDED.wind_mps, rain_mm = EXCLUDED.rain_mm;
            """, (match_id, temp, wind, rain, condition, 'WeatherAPI'))
            conn.commit()
        print(f"✅ Weather added for {city}: {condition}, {temp}°C")
    except Exception as e:
        logging.error(f"Failed to load weather for {city}: {e}")
        raise
