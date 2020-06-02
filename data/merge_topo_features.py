# Ten skrypt łączy rekordy dotyczące żlebów (zleby_scraped.txt) ze innymi rekordami dotyczącymi
# topografii terenu (almost_topo_features.txt).

# --- POBRANIE REKORDOW Z PLIKU almost_topo_features.txt ---
f = open("almost_topo_features.txt", 'r')
data = f.readlines()

records = {} # słownik zawierający rekord odpowiadający danemu obszarowi jednostkowemu

for line in data:
    l = line.split(',')
    area_name = l[0]

    # zakładamy, że na obszarze nie ma żlebu
    l.insert(1, "False")
    records[area_name] = l[1 : ]

# --- DODANIE DO REKORDÓW INFORMACJI Z PLIKU zleby_scraped.txt ---
f = open("zleby_scraped.txt", 'r')
data = f.readlines()

for line in data:
    l = line.split(',')
    area_name = l[0]

    if area_name in records:
        records[area_name][0] = "True"

# --- ZAPISANIE NOWYCH REKORDÓW DO FINALNEGO PLIKU topo_features.txt ---
f = open("topo_features.txt", 'w')
for key in records:
    to_write = key + ',' + ','.join(records[key])
    f.write(to_write)
