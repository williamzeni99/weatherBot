import requests

from geopy.geocoders import Nominatim

loc = Nominatim(user_agent="GetLoc")


def get_coordinates(city_name: str):
    city_url = 'http://api.openweathermap.org/geo/1.0/direct?q=' + city_name + '&limit=1&appid=' + api_key
    response = requests.get(city_url)
    city_data = response.json()

    if len(city_data) == 0:
        raise Exception(f"Error 400 - City {city_name} not found")

    return city_data

