# Ten skrypt pobiera aktualizowane na bieżąco dane pogodowe z serwera, łączy je
# z danymi dotyczącymi topografii i przy pomocy drzewa decyzyjnego zwraca stopień zagrożenia
# dla każdego z obszarów.
# Jeżeli z serwerem będzie wszystko spoko, to możemy te wszystkie obliczenia robić na serwerze.

# TODO:
# pobierz plik z serwera

# --- WCZYTAJ DANE LOKALNE I UTWÓRZ SŁOWNIK ---
import os
from pathlib import Path

path = str(Path(os.getcwd()).parent) + "/data/topo_features.txt"
f = open(path, 'r')
data = f.readlines()

records = {}

for line in data:
    l = line.split(',')
    records[l[0]] = l[1 : ]

# --- DODAJEMY INFORMACJĘ O PORZE ROKU ---
from datetime import date

today = str(date.today()).split('-')
month = int(today[1])
day = int(today[2])

if month == 6 and day >= 22 or month in (7, 8) or month == 9 and day <= 22:
    season = False # lato, pora roku nie stwarza zagrożenia
else:
    season = True

for area in records:
    records[area].append(season)

"""
# --- POBRANIE PLIKU Z SERWERA ---
import serverAPI
# ...
f = open(path, 'r')
data = f.readlines()

for line in data:
    l = line.split(',')
    records[l[0]] += l[1 : ] # otrzymujemy gotowe do predykcji rekordy
"""

# --- PREDYKCJA PRZY POMOCY DRZEWA ---
from decision_tree import build_tree, classify

# UWAGA! Przy każdym uruchomienu trenowane jest drzewo - jeżeli
# będzie to wolny proces, to można zapisać drzewo do pliku!
path = str(Path(os.getcwd()).parent) + "/data/artif_data.txt"
f = open(path, 'r')
training_data = [line.rstrip().split(',') for line in f]
header = training_data.pop(0)

tree = build_tree(training_data)

path = str(Path(os.getcwd()).parent) + "/data/predicted_risks.txt"
f = open(path, 'w')

for area in records:
    risk = list(classify(records[area]).keys())[0]
    f.write(area + ',' + risk + '\n')
