import os
from os.path import join, dirname
from requests import request
from pprint import pprint
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
APIkey = os.environ.get("APIKEY")


def convert_to_celcius(kelvin_value: float) -> float:
    return round(kelvin_value - 273.15, 2)


def get_weather(city, country="", state="", limit=1):
    if not city:
        return
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={APIkey}"
    response = request(method="GET", url=url)
    try:
        response = response.json()[0]
    except:
        return
    lat, lon = response["lat"], response["lon"]

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APIkey}"
    response = request(method="GET", url=url)
    response = response.json()
    temp = convert_to_celcius(response["main"]["temp"])
    state = response["weather"][0]["description"]
    return {"city": city, "temp": temp, "state": state}


if __name__ == "__main__":
    _city = input("Type a city name: ")
    pprint(get_weather(city=_city))
