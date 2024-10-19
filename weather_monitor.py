import requests
import sqlite3
from datetime import datetime
import time
from pushbullet import Pushbullet

# OpenWeatherMap API key and configuration
API_KEY = '21f028537f44174d14212392c697ed58'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
TEMP_THRESHOLD = 25  # User-configurable temperature threshold in Celsius
CHECK_INTERVAL = 300  # Interval to check weather data (5 minutes)

# Database configuration
DB_NAME = 'C:\\Users\\hp\\Documents\\weather_data.db' 

# Pushbullet API key
PUSHBULLET_API_KEY = 'o.t5urp3cdD6blJzvRPZTPy9ARlAldc9Bx'
pb = Pushbullet(PUSHBULLET_API_KEY)


def send_pushbullet_alert(message):
    """Send alert using Pushbullet."""
    try:
        pb.push_note("Test Alert", message)
        print("Pushbullet alert sent successfully.")
    except Exception as e:
        print(f"Failed to send Pushbullet alert: {e}")

# Test the Pushbullet notification
send_pushbullet_alert("This is a test notification from Python.")



def fetch_weather_data(city):
    """Fetch weather data from OpenWeatherMap API."""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve weather data for {city}: {response.status_code}")
        return None

def convert_k_to_c(temp_k):
    """Convert temperature from Kelvin to Celsius."""
    return temp_k - 273.15

def store_weather_data(city, temperature, feels_like, weather_condition):
    """Store weather data in SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Only create the table if it doesn't exist (no need to drop it)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT,
            temperature REAL,
            feels_like REAL,
            weather_condition TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        INSERT INTO weather (city, temperature, feels_like, weather_condition)
        VALUES (?, ?, ?, ?)
    ''', (city, temperature, feels_like, weather_condition))
    conn.commit()
    conn.close()
    print(f"Data for {city} inserted successfully.")



def update_daily_summary(city, temperature, weather_condition):
    """Update daily weather summary with aggregate data."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Add the condition_count column if it does not exist
    try:
        cursor.execute('ALTER TABLE daily_summary ADD COLUMN condition_count INTEGER DEFAULT 1')
    except sqlite3.OperationalError:
        # Column already exists, so we pass
        pass
    
    today = datetime.now().date()
    
    # Create the daily summary table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            city TEXT,
            date DATE,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT,
            condition_count INTEGER DEFAULT 1
        )
    ''')
    
    # Check if today's summary exists for the city
    cursor.execute('''
        SELECT avg_temp, max_temp, min_temp, dominant_condition, condition_count FROM daily_summary
        WHERE city = ? AND date = ?
    ''', (city, today))
    
    row = cursor.fetchone()
    
    if row:
        avg_temp, max_temp, min_temp, dominant_condition, condition_count = row
        new_avg_temp = ((avg_temp * condition_count) + temperature) / (condition_count + 1)
        new_max_temp = max(max_temp, temperature)
        new_min_temp = min(min_temp, temperature)
        
        # Update the weather condition count and determine the dominant one
        if weather_condition == dominant_condition:
            condition_count += 1
        else:
            condition_count = 1  # Reset count if the condition changes
        
        cursor.execute('''
            UPDATE daily_summary
            SET avg_temp = ?, max_temp = ?, min_temp = ?, dominant_condition = ?, condition_count = ?
            WHERE city = ? AND date = ?
        ''', (new_avg_temp, new_max_temp, new_min_temp, weather_condition, condition_count, city, today))
    else:
        # Insert a new record if no summary exists for today
        cursor.execute('''
            INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition, condition_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (city, today, temperature, temperature, temperature, weather_condition, 1))
    
    conn.commit()
    conn.close()
    print(f"Daily summary for {city} updated successfully.")




# Dictionary to track consecutive temperature breaches per city
consecutive_breaches = {city: 0 for city in CITIES}

def check_alerts(city, temperature, weather_condition):
    """Check if any alerts need to be sent."""
    if temperature > TEMP_THRESHOLD:
        alert_message = f"Alert for {city}: Temperature exceeded {TEMP_THRESHOLD}°C! Current temperature: {temperature:.2f}°C with {weather_condition}."
        print(alert_message)  # Log to console
        send_pushbullet_alert(alert_message)
    else:
        print(f"No alert: {city} temperature {temperature:.2f}°C below threshold.")




def main():
    """Main function to run the weather monitoring system."""
    while True:
        for city in CITIES:
            weather_data = fetch_weather_data(city)
            if weather_data:
                temp_k = weather_data['main']['temp']
                feels_like_k = weather_data['main']['feels_like']
                weather_condition = weather_data['weather'][0]['main']
                
                temperature = convert_k_to_c(temp_k)
                feels_like = convert_k_to_c(feels_like_k)
                
                store_weather_data(city, temperature, feels_like, weather_condition)
                
                # Pass both temperature and weather_condition
                update_daily_summary(city, temperature, weather_condition)
                
                check_alerts(city, temperature, weather_condition)
        
        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    main()
