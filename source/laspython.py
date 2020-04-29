import numpy as np
import pylas
import time
import pyowm

las = pylas.read('M-34-101-A-c-3-2-4.las')
print("Obszar wokół szczytu Miedziane(2233m.n.p.m.)")
print("Wersja pliku .las: ", las.header.scales)
print("Ilość wymiarów punktów: ", las.point_format)
print("Ilość punktów w pliku: ", las.header.point_count)
print("Wysokość maksymalna: ", las.z.max())
print("Wysokość minimalna: ",las.z.min())
print("Maksymalna różnica wysokości: ", las.z.max() - las.z.min())

pt_format = las.points_data.point_format
print(las.intensity)

# import pyowm
#
# owm = pyowm.OWM('7202a85833f71127c0a0b4fefc86ea2a')  # You MUST provide a valid API key
# # Aktualna temperatura w Krakowie
# observation = owm.weather_at_place('Krakow,PL')
# w = observation.get_weather()
# print(w)
#
# temp = w.get_temperature()  # domyślnie w Kelvinach leci
#
# print(w.get_temperature('celsius')["temp"])  # get_temperature zwraca słownik, pary klucz:wartość
# print(w.get_clouds())
# # Search current weather observations in the surroundings of
# # lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
# observation_list = owm.weather_around_coords(49.187922, 20.065686)
#
# print(observation_list[1].get_location())
#
# time.sleep(5)
