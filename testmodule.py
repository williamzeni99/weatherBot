import weather_module as w
import geoloc_module as g


def main():
    city = input("City name: ")

    try:
        coordinates = g.get_coordinates(city)
        data = w.get_weather_data(coordinates)
        print(w.print_weather_data(data))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
