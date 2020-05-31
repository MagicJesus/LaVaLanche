# --- POBRANIE ODPOWIEDNICH WSPÓŁRZĘDNYCH DLA OBSZARÓW ---
from selenium import webdriver # allows to use a browser
from bs4 import BeautifulSoup # allows to parse HTML
import pandas as pd # allows to export gathered data to .csv

f = open("latslongs.txt", "w")
f.write("area_name,N_lat,S_lat,W_long,E_long\n")

driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.get("file:///home/dittohead/Sym/data_extracted2.html")
driver_2 = webdriver.Chrome("/usr/bin/chromedriver")

content = driver.page_source
soup = BeautifulSoup(content, features = "lxml")

for link in soup.find_all('a'):
    driver_2.get(link.get('href'))

    content = driver_2.page_source
    soup_temp = BeautifulSoup(content, features = "lxml")

    f.write(soup_temp.title.text.split(',')[3].strip() + ',')

    # [N_lat, S_lat]
    for el in soup_temp.findAll("span", {"class": "latitude"}):
        f.write(el.text + ',')

    # [W_long, E_long]
    temp_str = ""
    for el in soup_temp.findAll("span", {"class": "longitude"}):
        temp_str += el.text + ','
    temp_list = list(temp_str)
    temp_list[-1] = '\n'
    temp_str = "".join(temp_list)
    f.write(temp_str)


temp_list[-1] = '\n'
temp_str = "".join(temp_list)
f.write(temp_str)
