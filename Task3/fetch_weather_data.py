import requests
import psycopg2
from datetime import datetime
import time

DB_HOST = "ep-noisy-lake-a8k78ama-pooler.eastus2.azure.neon.tech"
DB_NAME = "playground"
DB_USER = "shashank"
DB_PASSWORD = "C0nsult@nt"

API_KEY = "2a8e50ff40b7a51fd0fcd990420b686c"
CITY = "London"
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def fetch_weather():
    """Fetch weather data from OpenWeather API"""
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"⚠️ API Error: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        return None

def insert_into_db(weather_data):
    """Insert fetched weather data into PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        weather_desc = weather_data["weather"][0]["description"]
        wind_speed = weather_data["wind"]["speed"]
        timestamp = datetime.now()

        cur.execute("""
            INSERT INTO ml.weather_forecast (city, country, temperature, humidity, weather_description, wind_speed, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (city, country, temperature, humidity, weather_desc, wind_speed, timestamp))

        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Weather data for {city}, {country} inserted successfully at {timestamp}!")

    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    print("🌤️ Weather data fetcher started! Press Ctrl+C to stop.")
    while True:
        weather = fetch_weather()
        if weather:
            insert_into_db(weather)
        print("⏳ Waiting for 1 hour before the next update...\n")
        time.sleep(3600)
