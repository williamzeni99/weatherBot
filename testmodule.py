import weather_module as w



def main():
    city = input("City name: ")

    try:
        coordinates = w.get_coordinates(city)
        data = w.get_weather_data(coordinates)
        print(data)
        print(w.print_weather_data(data))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
