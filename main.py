import streamlit as st
import requests  # type: ignore
import os
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv(override=True)
API_KEY = os.getenv("TOMORROW_API_KEY")

# Streamlit page config
st.set_page_config(page_title="Weather App", page_icon="🌦️", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .weather-card {
        background-color: #3c6382;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 2px 2px 15px rgba(255, 255, 255, 0.3);
        color: white;
        text-align: center;
        width: 100%;
        margin: auto;
    }
    .small-text {
        font-size: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.title("🌦️ Interactive Weather Web App")

# User input for city name
city = st.text_input("📍 Enter City Name", "New York")


# Function to get latitude and longitude from city name
def get_lat_lon(city):
    geocode_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"

    headers = {
        "User-Agent": "WeatherApp/1.0 (contact: afifaak23@gmail.com)"  # Replace with your email
    }

    response = requests.get(geocode_url, headers=headers)
    
    try:
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
        else:
            return None, None
    except requests.exceptions.JSONDecodeError:
        return None, None


# Function to fetch weather data
def get_weather(lat, lon):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={API_KEY}"
    response = requests.get(url)

    # Debugging output
    print(f"API Status Code: {response.status_code}")
    print("Raw API Response:", response.text)

    if response.status_code != 200 or not response.text.strip():
        return None  # Return None if API fails

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return None  # Return None if JSON parsing fails


if st.button("🔍 Get Weather"):
    if city:
        lat, lon = get_lat_lon(city)

        if lat and lon:
            data = get_weather(lat, lon)

            if data and "data" in data and "values" in data["data"]:
                weather_data = data["data"]["values"]
                temp = weather_data.get("temperature", "N/A")
                humidity = weather_data.get("humidity", "N/A")
                wind_speed = weather_data.get("windSpeed", "N/A")
                weather_condition = weather_data.get("weatherCode", "Unknown")

                # Display weather data (without time)
                st.markdown(
                    f"""
                    <div class='weather-card'>
                        <h2>🌍 {city}</h2>
                        <p style="font-size: 50px; font-weight: bold; color: #ffcc00; margin: 10px 0;">{temp}°C</p>
                        <p class="small-text">🌤 Condition: {weather_condition}</p>
                        <p class="small-text">💧 Humidity: {humidity}%</p>
                        <p class="small-text">🌬 Wind Speed: {wind_speed} m/s</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("❌ Could not fetch weather data. Try again later.")
        else:
            st.error("❌ City not found! Please enter a valid city name.")
    else:
        st.warning("⚠️ Please enter a city name.")
