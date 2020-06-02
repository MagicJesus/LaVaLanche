# Ten skrypt pobiera informacje dotyczące występowania obiektów na obszarach jednostkowych
# korzystając z pliku links.html zawierającego odpowiednie linki do stron dostawcy plików las.
# Obiekty to np. szczyty i znane miejsca, które ułatwiają orientację, jakiego obszaru dotyczy zagrożenie.

from selenium import webdriver # zautomatyzowane użycie przeglądarki
from bs4 import BeautifulSoup # analiza kodu HTML
import re # regexp

from create_coord_dict import get_centers
coord_dict = get_centers()

f = open("obiekty_scraped.txt", "w")

# --- OTWARCIE W PRZEGLĄDARCE PLIKU links.html I POBRANIE ZAWARTOŚCI STRONY ---
driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.get("file:///home/dittohead/Sym/links.html")
driver_2 = webdriver.Chrome("/usr/bin/chromedriver")

content = driver.page_source
soup = BeautifulSoup(content, features = "lxml")

# --- OTWARCIE W PRZEGLĄDARCE KOLEJNYCH STRON ODPOWIADAJĄCYCH DUŻYM OBSZAROM I POBRANIE ZAWARTOŚCI STRONY ---
for link in soup.find_all('a'):
    driver_2.get(link.get('href'))

    content = driver_2.page_source
    soup_temp = BeautifulSoup(content, features = "lxml")

    area_name = soup_temp.title.text.split(',')[3].strip()
    (lat_center, long_center) = coord_dict[area_name]

    # --- OTWARCIE W PRZEGLĄDARCE KOLEJNYCH STRON ODPOWIADAJĄCYCH OBIEKTOM FIZJOGRAFICZNYM ---
    l = soup_temp.body.findAll('a')
    for a in l:
        if re.match("https://pzgik.geoportal.gov.pl/prng/ObiektFizjograficzny", a["href"]):
            driver_2.get(a["href"])
            content = driver_2.page_source
            soup_temp2 = BeautifulSoup(content, features = "lxml")

            object_name = soup_temp2.title.text

            # oblicz koordynaty i wyznacz odpowiednią nazwę obszaru jednostkowego, na którym znajduje się obiekt
            coords = soup_temp2.body.findAll(text = re.compile("[1-8][0-9]°"))
            lat = float(coords[0].split(' ')[0])
            long = float(coords[1].split(' ')[0])

            if lat > lat_center:
                if long > long_center:
                    sub_area = "-2"
                else:
                    sub_area = "-1"
            else:
                if long > long_center:
                    sub_area = "-4"
                else:
                    sub_area = "-3"

            to_write = area_name + sub_area + ',' + object_name + '\n'
            print(to_write)
            f.write(to_write)
