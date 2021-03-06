# Ten skrypt generuje rekordy (sztuczny zbiór danych) w oparciu o możliwe przyjmowane wartości (tworzy wszystkie
# możliwe kombinacje). Możliwe wartości oraz etykiety zostały opracowane ręcznie na podstawie polskich i zagranicznych
# publikacji.

# Rzeczywiste rekordy będą reprezentować poszczególne obszary Tatr (2km x 2km) - przykładowo, jeżeli na terenie
# nie występują odpowiednio duże formy wklęsłe, to atrybut form_terenu przyjmie wartość "plaska/wypukla"
from itertools import product

# --- OKREŚLENIE MOŻLIWYCH WARTOŚCI CECH ---
# True - wartość cechy zwiększa ryzyko, False - wartość cechy zmniejsza ryzyko.

form_terenu = [True, False] # True <=> forma wklesla
eksp_sloneczna = [True, False] # True <=> eksp_sloneczna IN (NE, W, E) dla stoków o nachyleniu (30, 40) stopni
nachylenie = [True, False] # True <=> Q1 (1. kwartyl) nachyleń >= 25 and Q3 nachyleń <= 50 stopni
pietro = [True, False] # True <=> pietro o ubogiej roslinosci, max_wysokość terenu >= 1600
wysokosc = [True, False] # True <=> Q1 (1. kwartyl) wysokości >= 1300 and Q3 wysokości <= 2100 metrów
pora_roku = [True, False] # True <=> pora_roku IN (jesien, zima, wiosna)

# dla opadów i wiatru zostaną przyjęte odpowiednie progi
deszcz48h = [True, False]
snieg48h = [True, False]
wiatr48h = [True, False]
wzr_temp = [True, False]

possible_vals = [form_terenu, eksp_sloneczna, nachylenie, pietro, wysokosc, pora_roku,
                    deszcz48h, snieg48h, wiatr48h, wzr_temp]
data = list(product(*possible_vals))

f = open("artif_data.txt", "w")
f.write("form_terenu, eksp_sloneczna, nachylenie, pietro, wysokosc, pora_roku, deszcz48h, snieg48h, wiatr48h, wzr_temp\n")

# --- NADANIE ODPOWIEDNICH ETYKIET ---
for record in data:
    if (not record[0] and not record[4]) or (not record[5] and not record[-3]) or (not record[-1] and not record[-2] and not record[-3] and not record[-4]):
        label = "brak"
    elif record[0] and record[1] and record[2] and record[3] and record[4] and record[5] and (record[6] or record[7] or record[8] or record[9]):
        label = "wysokie"
    else:
        label = "niskie/umiarkowane"

    record_labeled = list(record)
    for i in range(len(record_labeled)):
        if record_labeled[i]:
            record_labeled[i] = "True"
        else:
            record_labeled[i] = "False"

    record_labeled.append(label)

    # --- ZAPIS DO PLIKU artif_data.txt ---
    to_write = ",".join(record_labeled) + '\n'
    f.write(to_write)
