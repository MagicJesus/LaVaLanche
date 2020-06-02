# Ten skrypt oblicza współrzędne geograficzne środków dużych obszarów.

def get_centers():
    f = open("lats_longs_scraped.txt", 'r')
    data = f.readlines()

    del data[0] # pomijamy nagłówek pliku

    coords = {} # słownik zawierający 1 zestaw koordynatów dla wszystkich 2, 3 lub 4 obszarów

    for line in data:
        l = line.split(',')
        coords[l[0]] = ((float(l[1]) + float(l[2])) / 2, (float(l[3]) + float(l[4])) / 2)
        # coords[...] = (latitude, longitude)

    return coords
