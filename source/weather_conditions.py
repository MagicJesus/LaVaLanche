import pyowm
import os
import time


def extract_coords(map_name):

    if ".las" in map_name:
        map_name = map_name[0:16]
    else:
        map_name = map_name[0:16]
    file = open("..\\data\\lats_longs_scraped.txt")
    for line in file:
        if map_name in line:
            line = line[0:len(line) - 1]
            splited = line.split(",")
            coords = {
                    "N_lat": splited[1],
                    "S_lat": splited[2],
                    "W_long": splited[3],
                    "E_long": splited[4]
                    }
            break
    return coords


def get_weather_conditions(map_name):
    # stworz odpowiedni folder jeżeli nie istnieje
    if os.path.isdir("..\\data\\weather_data\\" + map_name[0:16]):
        pass
    else:
        path = "..\\data\\weather_data\\" + map_name[0:16]
        os.mkdir(path)

    # współrzędne obszaru i aktualny czas
    coords = extract_coords(map_name)
    czas_pomiaru = str(time.ctime()).split(" ")

    # inicjalizacja zmiennej pogodowej hehe i pobranie pogody
    owm = pyowm.OWM("7202a85833f71127c0a0b4fefc86ea2a")
    observation = owm.weather_around_coords(float(coords["N_lat"]), float(coords["W_long"]))

    # sprawdz czy bylo 6 pomiarów, jak bylo usun najstarszy
    data = os.listdir("..\\data\\weather_data\\" + map_name[0:16] + "\\")
    if len(data) >= 6:
        os.remove("..\\data\\weather_data\\" + map_name[0:16] + "\\" + data[0])
    # stworz plik z danymi z konkretnego dnia i zapisz w pliku
    filename = str(observation[0].get_weather().get_reference_time('date'))[0:10]
    data = open("..\\data\\weather_data\\" + map_name[0:16] + "\\" + filename + "_" + czas_pomiaru[3].replace(":", "-") + ".txt", "w+")
    data.write("Temperatura: " + str(observation[0].get_weather().get_temperature('celsius')['temp']) + "\n")
    data.write("Opad sniegu: " + str(observation[0].get_weather().get_snow()) + "\n")
    data.write("Wiatr[m/s]: " + str(observation[0].get_weather().get_wind('meters_sec')) + "\n")
    data.write("Opad deszczu: " + str(observation[0].get_weather().get_rain()) + "\n")
    print("end")


with open("..\\data\\lats_longs_scraped.txt") as file:
    file.readline()
    for line in file:
        get_weather_conditions(line.rstrip()[0:16])
