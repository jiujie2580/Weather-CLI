import json
import unittest
from unittest.mock import patch

import weather


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class WeatherTests(unittest.TestCase):
    def test_get_weather_formats_successful_response(self):
        payload = {"cod": 200, "weather": [{"description": "clear sky"}], "main": {"temp": 18.4}}
        with patch("weather.urlopen", return_value=FakeResponse(payload)):
            result = weather.get_weather("London", api_key="test-key")

        self.assertEqual(result, "London weather: clear sky, temperature: 18.4C")

    def test_get_weather_requires_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(weather.WeatherError, "OPENWEATHER_API_KEY"):
                weather.get_weather("London")

    def test_get_weather_reports_service_errors(self):
        payload = {"cod": "401", "message": "invalid api key"}
        with patch("weather.urlopen", return_value=FakeResponse(payload)):
            with self.assertRaisesRegex(weather.WeatherError, "invalid api key"):
                weather.get_weather("London", api_key="bad-key")


if __name__ == "__main__":
    unittest.main()
