import requests

# Enter your API key openweathermap.org
api_key = 'fe10eb2498e51eeb264ec71355e0f6fa'


# It provides array coordinates[ lat, lon] from a city name
def get_coordinates(city_name: str):
    city_url = 'http://api.openweathermap.org/geo/1.0/direct?q=' + city_name + '&limit=1&appid=' + api_key

    response = requests.get(city_url)
    city_data = response.json()

    if len(city_data) == 0:
        raise Exception(f"Error 400 - City {city_name} not found")

    lat = str(city_data[0]['lat'])
    lon = str(city_data[0]['lon'])

    city_data = [lat, lon]

    return city_data
