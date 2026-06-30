import requests

def get_coordinates(city: str) -> dict:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1}
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    if not data.get("results"):
        return {"error": f"City '{city}' not found"}

    r = data["results"][0]
    return {
        "city": r["name"],
        "country": r.get("country", ""),
        "latitude": r["latitude"],
        "longitude": r["longitude"]
    }

def get_weather(latitude: float, longitude: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,apparent_temperature,weather_code",
        "timezone": "auto"
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    current = data["current"]

    weather_descriptions = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
        3: "Overcast", 45: "Foggy", 51: "Light drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        80: "Rain showers", 95: "Thunderstorm"
    }
    code = current["weather_code"]

    # ✅ Weather alerts
    alerts = []
    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]

    if temp >= 38:
        alerts.append("⚠️ Extreme heat warning! Stay hydrated and avoid going out.")
    elif temp >= 35:
        alerts.append("🌡️ High temperature alert! Carry water if heading out.")
    if humidity >= 80:
        alerts.append("💧 Very high humidity! It will feel much hotter outside.")
    if wind >= 40:
        alerts.append("💨 Strong wind warning! Be cautious outdoors.")
    if code in [61, 63, 65, 80]:
        alerts.append("🌧️ Rain expected! Carry an umbrella.")
    if code == 95:
        alerts.append("⛈️ Thunderstorm warning! Avoid outdoor activities.")

    return {
        "temperature_c": temp,
        "feels_like_c": current["apparent_temperature"],
        "humidity_percent": humidity,
        "wind_speed_kmh": wind,
        "condition": weather_descriptions.get(code, "Unknown"),
        "alerts": alerts if alerts else ["✅ No weather alerts. Conditions are normal."]
    }

def get_forecast(latitude: float, longitude: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 5
    }
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    daily = data["daily"]

    weather_descriptions = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
        3: "Overcast", 45: "Foggy", 51: "Light drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        80: "Rain showers", 95: "Thunderstorm"
    }

    forecast = []
    for i in range(5):
        code = daily["weather_code"][i]
        rain_chance = daily["precipitation_probability_max"][i]

        day_alerts = []
        max_temp = daily["temperature_2m_max"][i]
        if max_temp >= 38:
            day_alerts.append("⚠️ Extreme heat")
        if rain_chance >= 70:
            day_alerts.append("🌧️ High rain chance")
        if code == 95:
            day_alerts.append("⛈️ Thunderstorm likely")

        forecast.append({
            "date": daily["time"][i],
            "max_temp_c": max_temp,
            "min_temp_c": daily["temperature_2m_min"][i],
            "condition": weather_descriptions.get(code, "Unknown"),
            "rain_chance_percent": rain_chance,
            "alerts": day_alerts
        })

    return {"forecast": forecast}