# Real-Time-Weather-Monitoring
This project implements a real-time weather monitoring system that fetches weather data from the OpenWeatherMap API, processes it to provide daily summaries, and sends alerts based on user-defined thresholds.

# Real-Time Weather Monitoring System

This project implements a real-time weather monitoring system that fetches weather data from the OpenWeatherMap API, processes it to provide daily summaries, and sends alerts based on user-defined thresholds.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Design Choices](#design-choices)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)

## Introduction

The Real-Time Weather Monitoring System continuously retrieves weather data for selected metros in India, calculates daily aggregates, and triggers alerts when specified thresholds are breached. The system aims to provide users with timely information about current weather conditions and potential alerts.

## Features

- Fetches real-time weather data for multiple cities using the OpenWeatherMap API.
- Converts temperature values from Kelvin to Celsius.
- Calculates daily weather summaries including average, maximum, and minimum temperatures, as well as dominant weather conditions.
- Sends notifications via Pushbullet when specified temperature thresholds are exceeded.
- Stores weather data and daily summaries in an SQLite database for persistence.

## Design Choices

1. **Architecture:**
   - **Modular Design:** The system is designed with a clear separation of concerns, breaking functionality into modules for data retrieval, processing, storage, and alerting. This allows for easier testing and maintenance.

2. **Data Handling:**
   - **API Integration:** The system uses the OpenWeatherMap API for fetching weather data, ensuring that users receive up-to-date information.
   - **SQLite for Storage:** An SQLite database is used for persistent storage of weather data and daily summaries, making the system lightweight and easy to manage without the need for a separate database server.

3. **Alerting System:**
   - The alerting mechanism uses Pushbullet for notifications, allowing users to receive real-time alerts on their devices.
   - Alerts are triggered based on configurable temperature thresholds, providing flexibility to users.

4. **Extensibility:**
   - The system is designed to easily integrate additional weather parameters (e.g., humidity, wind speed) and features (e.g., weather forecasts) in the future.

## Installation

To set up and run the application, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/weather-monitor.git
   cd weather-monitor
2. **Install Dependencies:**
Install the required Python packages using pip:
pip install requests pushbullet.py sqlite3

3.**Obtain API Keys:**

Sign up for an API key from OpenWeatherMap.
Create a Pushbullet account and generate an API key from the Pushbullet website.
Update Configuration:

Open the weather_monitor.py file and update the API_KEY and PUSHBULLET_API_KEY variables with your obtained keys.

The application will start fetching weather data for the specified cities at the configured interval (default: every 5 minutes). Alerts will be sent via Pushbullet when the defined temperature threshold is exceeded.

Dependencies
requests: For making HTTP requests to the OpenWeatherMap API.
pushbullet.py: For sending push notifications via Pushbullet.
sqlite3: For database management (part of Python’s standard library).

