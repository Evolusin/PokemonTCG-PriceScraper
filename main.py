import csv
import datetime

import requests
from bs4 import BeautifulSoup


class Product:
    def __init__(self, title, href):
        self.title = title
        self.href = href

    def setprice(self, price):
        self.price = price
    
    def scrap_price(self):
        page = requests.get(self.href)
        soup = BeautifulSoup(page.content, "html.parser")
        # Search for bdi tag inside of section class
        self.price = soup.find("section", class_="elementor-section elementor-top-section elementor-element elementor-element-2bdb3ad elementor-section-boxed elementor-section-height-default elementor-section-height-default").find("bdi").text
        # strip price from unnecessary characters
        self.price = self.price.replace("zł", "").replace(" ", "").replace(",", ".")
            
class CSV:
    def __init__(self):
        # generate csv file name with timestamp
        self.name = "products-" + datetime.datetime.now().strftime("%m-%d-%Y-%H") + ".csv"
        self.set_header()
        
    def set_header(self):
        with open(self.name, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Link", "Price"])

    def save(self, product):
        # save product on new line in csv file
        with open(self.name, "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([product.title, product.href, product.price])
            

def get_all_items(url):
    # Pobieranie strony
    page = requests.get(url)

    # Tworzenie obiektu BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    # Search for all products by div class
    products = soup.find_all("div", class_="woocommerce-loop-product__title")
    saver = CSV()
    for x in products:
        product = Product(x.text, x.find("a")["href"])
        product.scrap_price()
        # append product to csv file
        saver.save(product)
        
def get_all_pages():
    # Get all pages from main page
    page = requests.get("https://czteryszuflady.pl/sklep/kategorie/pokemon-tcg/page/1/")
    soup = BeautifulSoup(page.content, "html.parser")
    pages = soup.find("ul", class_="page-numbers").find_all("li")
    # extract only html links from pages
    for x in pages:
        if x.find("a") != None:
            print(x.find("a")["href"])
    # remove diu


get_all_pages()