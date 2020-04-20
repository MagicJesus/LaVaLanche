import os

directory = "D:\\Mapy Tatr\\A" # Ty na linusie to trzeba będzi zmieniać ścieżeczki :(

for filename in os.listdir(directory):
    if filename.endswith(".las"):
        print(filename)
        continue
    else:
        continue

# tutaj mój drogi dałbym funkcje np do otwierania plików z mapami, w innym można dać te do obliczania już zagrożenia
# tu ewentualnie mozna pogrupować mapki na kwadraty 4x4 zgodnie z nazewnictwem
# może dałoby się złączyć 4 pliczki w jeden czy coś? XD


def open_map(map_name):
    pass

