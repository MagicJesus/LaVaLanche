# 1. Wczytaj rekordy zawierające koordynaty graniczne dla większych obszarów (każdy z nich odpowiada 3 lub 4 obszarom
# autonomicznym).
# 2. Oblicz średnie koordynaty dla każdego większego obszaru i utwórz słownik.

f = open("lats_longs_scraped.txt", 'r')
data = f.readlines()

del data[0] # pomijamy nagłówek pliku

coords = {} # słownik zawierający 1 zestaw koordynatów dla wszystkich 2, 3 lub 4 obszarów

for line in data:
    l = line.split(',')
    coords[l[0]] = ((float(l[1]) + float(l[2])) / 2, (float(l[3]) + float(l[4])) / 2)
    # dict["name"] = (latitude, longitude)

for keys, values in coords.items():
    print(f"{keys}: {values}")
