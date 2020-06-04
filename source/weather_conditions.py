import pyowm
import os
import time


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
