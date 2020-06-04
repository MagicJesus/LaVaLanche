# Ten skrypt łączy pobrane dane pogodowe z danymi dotyczącymi topografii i przy pomocy drzewa decyzyjnego
# zwraca stopień zagrożenia dla każdego z obszarów.

import os
from pathlib import Path

# --- WCZYTAJ DANE LOKALNE I UTWÓRZ SŁOWNIK ---
def load_topo_data():
    path = str(Path(os.getcwd()).parent) + "/data/topo_features.txt"
    f = open(path, 'r')
    data = f.readlines()

    records = {}

    for line in data:
        l = line.split(',')
        records[l[0]] = l[1 : ]

    return records

# --- DODAJE INFORMACJĘ O PORZE ROKU ---
from datetime import date

def add_season(records):
    today = str(date.today()).split('-')
    month = int(today[1])
    day = int(today[2])

    if month == 6 and day >= 22 or month in (7, 8) or month == 9 and day <= 22:
        season = False # lato, pora roku nie stwarza zagrożenia
    else:
        season = True

    for area in records:
        records[area].append(season)

# --- STWORZENIE FINALNYCH REKORDÓW (CECHY TOPOGRAFICZNE + POGODOWE) ---
def add_weather(topo_records, weather_records):
    final_records = {}
    for area in topo_records:
        final_records[area] = topo_records[area] + weather_records[area] # otrzymujemy gotowe do predykcji rekordy

    return final_records

# --- PREDYKCJA PRZY POMOCY DRZEWA ---
from decision_tree import build_tree, classify

def get_risks(records):
    # UWAGA! Przy każdym uruchomienu trenowane jest drzewo - jeżeli
    # będzie to wolny proces, to można zapisać drzewo do pliku!
    path = str(Path(os.getcwd()).parent) + "/data/artif_data.txt"
    f = open(path, 'r')
    training_data = [line.rstrip().split(',') for line in f]
    header = training_data.pop(0)

    tree = build_tree(training_data)

    predicted_risks = {}

    for area in records:
        predicted_risks[area] = list(classify(records[area]).keys())[0]

    return predicted_risks
