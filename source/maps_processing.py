import os

directory = "..\\data\\maps_sequence.txt" # Ty na linusie to trzeba będzi zmieniać ścieżeczki :(
button_map = "button_map.txt"

# for filename in os.listdir(directory):
#     if filename.endswith(".las"):
#         #print(filename)
#         continue
#     else:
#         continue

# with open(button_map) as buttonmap:
#      for line in buttonmap:
#         linia = line
#         for ch in linia:
#             if ch == "1":
#                 print("gu ", end='')
#             elif '\n' in ch:
#                 print('')
#             elif ch == "0":
#                 print("no ", end='')

mapki = open(directory)
for line in mapki:
    print(line.rstrip(), end=".las\n")


        # for ch in line:
        #     if '\n' in ch:
        #         print("")
        #     else:
        #         print(ch, end='')

# tutaj mój drogi dałbym funkcje np do otwierania plików z mapami, w innym można dać te do obliczania już zagrożenia
# tu ewentualnie mozna pogrupować mapki na kwadraty 4x4 zgodnie z nazewnictwem
# może dałoby się złączyć 4 pliczki w jeden czy coś? XD


def open_map(map_name):
    pass

