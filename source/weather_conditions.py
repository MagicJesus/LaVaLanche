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
    # create a folder if it does not exist
    if os.path.isdir("..\\data\\weather_data\\" + map_name[0:16]):
        pass
    else:
        path = "..\\data\\weather_data\\" + map_name[0:16]
        os.mkdir(path)

    # coordinates of a given area and the time of measurement
    coords = extract_coords(map_name)
    czas_pomiaru = str(time.ctime()).split(" ")

    # getting the weather data
    owm = pyowm.OWM("7202a85833f71127c0a0b4fefc86ea2a")
    observation = owm.weather_around_coords(float(coords["N_lat"]), float(coords["W_long"]))

    # check if there were 6 measurements, if yes, delete the oldest one
    data = os.listdir("..\\data\\weather_data\\" + map_name[0:16] + "\\")
    if len(data) >= 6:
        os.remove("..\\data\\weather_data\\" + map_name[0:16] + "\\" + data[0])
    # create a file containing up to date weather data
    filename = str(observation[0].get_weather().get_reference_time('date'))[0:10]
    data = open("..\\data\\weather_data\\" + map_name[0:16] + "\\" + filename + "_" + czas_pomiaru[3].replace(":", "-") + ".txt", "w+")
    data.write(str(observation[0].get_weather().get_temperature('celsius')['temp']) + "\n")
    data.write(str(observation[0].get_weather().get_snow()) + "\n")
    data.write(str(observation[0].get_weather().get_wind('meters_sec')) + "\n")
    data.write(str(observation[0].get_weather().get_rain()) + "\n")
    print("end")

#
# with open("..\\data\\lats_longs_scraped.txt") as file:
#     file.readline()
#     for line in file:
#         get_weather_conditions(line.rstrip()[0:16])


def weather_analysis(map_name):
    path = "..\\data\\weather_data\\" + map_name[0:16]
    weather = {}
    temperature = []
    snow = []
    wind = []
    rain = []
    files = os.listdir(path)
    for file in files:
        handle = open(path + "\\" + file)
        temperature.append(handle.readline().rstrip())
        snow.append(handle.readline().rstrip())
        wind.append(handle.readline().rstrip())
        rain.append(handle.readline().rstrip())
        handle.close()

    # temperature stats
    mean = []
    for t in temperature:
        mean.append(float(t))
    avg = sum(mean)/len(mean)
    if min(mean)*max(mean) < 0 and avg > 0:
        weather["wzr_temp"] = True
    else:
        weather["wzr_temp"] = False
    # snow stats
    weather["snieg48h"] = False
    overall_snow_layer = 0.0
    for s in snow:
        if 'h' in s:
            amount_in_mm = s[7:11]
            if '}' in amount_in_mm:
                amount_in_mm = amount_in_mm[0:3]
            overall_snow_layer += float(amount_in_mm)
        elif s.replace("{}", "none") == "none":
            overall_snow_layer += 0
    if overall_snow_layer > 200:
        weather["snieg48h"] = True

    # rain stats
    weather["deszcz48h"] = False
    for r in rain:
        if s.replace("{}", "none") != "none":
            weather["deszcz48h"] = True
    # wind stats
    weather["wiatr48h"] = False
    for w in wind:
        if float(w[10:13]) >= 13.0:
            weather["wiatr48h"] = True

    print(map_name, weather)


# mapy = os.listdir("..\\..\\maps\\A")
# for m in mapy:
#     weather_analysis(m)
weather_analysis("M-34-100-B-a-1-2-1")
