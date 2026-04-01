"""
Weather tool — fetches current weather via OpenWeatherMap API.
Requires OPENWEATHER_API_KEY in .env
"""
import re
import os
import requests


def _extract_city(query: str) -> str:
    match = re.search(r"(?:weather\s+(?:in|for|at)\s+)(.+)", query, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Fallback: last word(s) after 'weather'
    match2 = re.search(r"weather\s+(.+)", query, re.IGNORECASE)
    if match2:
        return match2.group(1).strip()
    return ""


def run(query: str) -> str:
    city = _extract_city(query)
    if not city:
        return "Please specify a city, e.g. 'weather in Delhi'."

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "OPENWEATHER_API_KEY not set in .env — cannot fetch weather."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        return (
            f"Weather in {data['name']}, {data['sys']['country']}:\n"
            f"  {desc}, {temp}°C (feels like {feels}°C), humidity {humidity}%"
        )
    except requests.HTTPError as e:
        return f"Weather API error: {e.response.status_code} — {e.response.text}"
    except Exception as exc:
        return f"Failed to fetch weather: {exc}"
