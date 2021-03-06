import pyowm
import os
import re
import time
from pathlib import Path


def single_weather_analysis(map_name):
    regex_pattern = '[0-9]+\.?[0-9]*'
    path = "../data/weather_data/" + map_name[0:16]
    weather = {}
    temperature = []
    snow = []
    wind = []
    rain = []
    final_list = []
    files = os.listdir(path)
    for file in files:
        handle = open(path + '/' + file)
        temperature.append(handle.readline().rstrip())
        snow.append(handle.readline().rstrip())
        wind.append(handle.readline().rstrip())
        rain.append(handle.readline().rstrip())
        handle.close()

    # Przetwarzanie danych
    mean = []
    for t in temperature:
        mean.append(float(t))
    avg = sum(mean)/len(mean)
    if min(mean)*max(mean) < 0 and avg > 0:
        weather["wzr_temp"] = 'True'
    else:
        weather["wzr_temp"] = 'False'
    # snow stats
    weather["snieg48h"] = 'False'
    overall_snow_layer = 0.0
    for s in snow:
        if 'h' in s:
            amount_in_mm = re.findall(regex_pattern, s)[1]
            overall_snow_layer += float(amount_in_mm)
        elif s.replace("{}", "none") == "none":
            overall_snow_layer += 0
    if overall_snow_layer > 200:
        weather["snieg48h"] = 'True'

    # rain stats
    weather["deszcz48h"] = 'False'
    for r in rain:
        if '{}' not in r:
            weather["deszcz48h"] = 'True'
    # wind stats
    weather["wiatr48h"] = 'False'
    for w in wind:
        if float(re.findall(regex_pattern, w)[0]) >= 13.0:
            weather["wiatr48h"] = 'True'

    final_list.append(weather["deszcz48h"])
    final_list.append(weather["snieg48h"])
    final_list.append(weather["wiatr48h"])
    final_list.append(weather["wzr_temp"])

    return final_list


def overall_weather_analysis():
    path = str(Path(os.getcwd()).parent) + "/data/maps_sequence.txt"
    f = open(path, 'r')
    maps = f.readlines()

    weather_records = {}

    for m in maps:
        weather_records[m[0:18]] = single_weather_analysis(m)
    return weather_records
