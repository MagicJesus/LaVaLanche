import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as Soup


def scrap_coordinates(my_url):

    u_client = urlopen(my_url)
    dane_html = u_client.read()
    parsed_html = Soup(dane_html, "html.parser")

    long_geo = parsed_html.findAll("span", {"class": "longitude"})
    lat_geo = parsed_html.findAll("span", {"class": "latitude"})

    coordinates = {"North lat": lat_geo[0].text,
                   "West long": long_geo[0].text,
                   "South lat": lat_geo[1].text,
                   "East long": long_geo[1].text
                   }

    print(coordinates)
    u_client.close()
    return coordinates


scrap_coordinates("https://pzgik.geoportal.gov.pl/semantic-metadata/orto/dataset/8a73a08f-1768-11e6-ae06-b870f44b6730?fbclid=IwAR2qs4oGezFVmnrVkMHIZ95-HfIeK5pheoDKd6gLKn2-MSz9T9nUBMDcVjY")