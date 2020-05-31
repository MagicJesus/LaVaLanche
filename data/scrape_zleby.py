# --- PRZYPORZĄDKOWANIE OBSZAROM JEDNOSTKOWYM EWENTUALNYCH ŻLEBÓW ---
from selenium import webdriver # allows to use a browser
from bs4 import BeautifulSoup # allows to parse HTML
import pandas as pd # allows to export gathered data to .csv
import re # regexp

from create_coord_dict import get_centers
coord_dict = get_centers()

f = open("zleby_scraped.txt", "w")

driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.get("file:///home/dittohead/Sym/links.html")
driver_2 = webdriver.Chrome("/usr/bin/chromedriver")

content = driver.page_source
soup = BeautifulSoup(content, features = "lxml")

for link in soup.find_all('a'):
    driver_2.get(link.get('href'))

    content = driver_2.page_source
    soup_temp = BeautifulSoup(content, features = "lxml")

    area_name = soup_temp.title.text.split(',')[3].strip()
    (lat_center, long_center) = coord_dict[area_name]

    l = soup_temp.body.findAll('a')
    for a in l:
        if re.match("https://pzgik.geoportal.gov.pl/prng/ObiektFizjograficzny", a["href"]):
            # przechodzimy do kolejnej podstrony
            driver_2.get(a["href"])
            content = driver_2.page_source
            soup_temp2 = BeautifulSoup(content, features = "lxml")

            zleb_name = soup_temp2.body.findAll(text = re.compile(" Żleb$")) # czy to strona dotycząca żlebu?
            if zleb_name:
                # oblicz koordynaty i wyznacz odpowiednią nazwę obszaru jednostkowego
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

                f.write(area_name + sub_area + ',' + zleb_name[0] + '\n')
