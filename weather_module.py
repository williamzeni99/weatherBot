import requests
import geoloc_module as g
from datetime import datetime

# Enter your API key openweathermap.org
api_key = 'fe10eb2498e51eeb264ec71355e0f6fa'


# Get the time from utc and timezone values provided
# pass the value as utc + timezone (both are UTC timestamp)
def time_from_utc_with_timezone(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()


def get_weather_data(city_name: str):

    city_data = g.get_coordinates(city_name)
    lat = str(city_data[0]['lat'])
    lon = str(city_data[0]['lon'])

    weather_url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&appid=' + api_key
    response = requests.get(weather_url)
    weather_data = response.json()

    if weather_data['cod'] == 200:
        return weather_data
    else:
        raise Exception("Error 401 - Weather data cannot be provided")


def print_weather_data(data: str):
    kelvin = 273.15  # Temperature shown here is in Kelvin and I will show in Celsius
    city_name = data['name']
    country = data['sys']['country']
    temp = int(float(data['main']['temp']) - kelvin)
    feels_like_temp = int(float(data['main']['feels_like']) - kelvin)
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed'] * 3.6
    sunrise = data['sys']['sunrise']
    sunset = data['sys']['sunset']
    timezone = data['timezone']
    cloudy = data['clouds']['all']
    description = data['weather'][0]['description']

    sunrise_time = time_from_utc_with_timezone(sunrise + timezone)
    sunset_time = time_from_utc_with_timezone(sunset + timezone)

    s = f"Weather Information for City: {city_name} - {country} \n"
    s += f"Temperature (Celsius): {temp}\n"
    s += f"Feels like in (Celsius): {feels_like_temp}\n"
    s += f"Pressure: {pressure} hPa\n"
    s += f"Humidity: {humidity}%\n"
    s += "Wind speed: {0:.2f} km/hr".format(wind_speed) + "\n"
    s += f"Sunrise at {sunrise_time} and Sunset at {sunset_time}\n"
    s += f"Cloud: {cloudy}%\n"
    s += f"Info: {description}\n"

    return s

    # print(f"Weather Information for City: {city_name} - {country}")
    # print(f"Temperature (Celsius): {temp}")
    # print(f"Feels like in (Celsius): {feels_like_temp}")
    # print(f"Pressure: {pressure} hPa")
    # print(f"Humidity: {humidity}%")
    # print("Wind speed: {0:.2f} km/hr".format(wind_speed))
    # print(f"Sunrise at {sunrise_time} and Sunset at {sunset_time}")
    # print(f"Cloud: {cloudy}%")
    # print(f"Info: {description}")
