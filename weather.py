from __future__ import annotations

import argparse
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_TIMEOUT = 10


class WeatherError(Exception):
    """Raised when weather data cannot be fetched or parsed."""


def _load_json(url: str, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    try:
        with urlopen(url, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raw_error = exc.read().decode("utf-8", errors="replace")
        message = exc.reason
        if raw_error:
            try:
                payload = json.loads(raw_error)
            except json.JSONDecodeError:
                message = raw_error
            else:
                message = payload.get("message", exc.reason)
        raise WeatherError(f"weather service error: {message}") from exc
    except URLError as exc:
        raise WeatherError(f"network error: {exc.reason}") from exc
    except TimeoutError as exc:
        raise WeatherError("network timeout") from exc
    except json.JSONDecodeError as exc:
        raise WeatherError("weather service returned invalid data") from exc


def get_weather(city: str, api_key: str | None = None, timeout: int = DEFAULT_TIMEOUT) -> str:
    api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise WeatherError("set OPENWEATHER_API_KEY before running this command")

    query = urlencode({"q": city, "appid": api_key, "units": "metric"})
    data = _load_json(f"{BASE_URL}?{query}", timeout=timeout)

    if str(data.get("cod")) != "200":
        raise WeatherError(str(data.get("message", "weather lookup failed")))

    weather_items = data.get("weather") or []
    main = data.get("main") or {}
    if not weather_items or "temp" not in main:
        raise WeatherError("weather service response is missing required fields")

    description = weather_items[0].get("description", "unknown")
    temp = float(main["temp"])
    warning = " (high temperature warning!)" if temp > 30 else ""
    return f"{city} weather: {description}, temperature: {temp:.1f}C{warning}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Look up current weather for a city.")
    parser.add_argument("city", nargs="+", help="City name, for example: London or Beijing")
    parser.add_argument(
        "--api-key",
        help="OpenWeather API key. If omitted, OPENWEATHER_API_KEY is used.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Request timeout in seconds.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    city = " ".join(args.city)

    try:
        print(get_weather(city, api_key=args.api_key, timeout=args.timeout))
        return 0
    except WeatherError as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
