from selenium import webdriver # allows to use a browser
from bs4 import BeautifulSoup # allows to parse HTML
import pandas as pd # allows to export gathered data to .csv
import re # regexp

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

    l = soup_temp.body.findAll(text = re.compile(" Żleb$"))
    if(l):
        print(l)
        f.write(soup_temp.title.text.split(',')[3].strip() + '\n')
