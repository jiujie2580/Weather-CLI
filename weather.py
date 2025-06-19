import requests
import sys

# 注意：把YOUR_API_KEY改成你自己的key（没key先随便填，如：12345）
API_KEY = "12345"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        if data["cod"] != 200:
            return f"Error: {data['message']}"
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{city}天气: {weather}, 温度: {temp}℃{' (高温预警!)' if temp > 30 else ''}"
    except Exception as e:
        return f"查询失败: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python weather.py [城市名称]")
    else:
        city = " ".join(sys.argv[1:])
        print(get_weather(city))