import csv
import datetime
import json
import os

import requests
from bs4 import BeautifulSoup


class Product:
    def __init__(self, title, href):
        self.title = title
        self.href = href

    def scrap_price(self):
        page = requests.get(self.href)
        soup = BeautifulSoup(page.content, "html.parser")
        # Search for bdi tag inside of section class but ignore if span class is inside del tag and look for the next bdi tag
        # iterate over p tag inside of section class
        rows = soup.find("section", class_="elementor-section elementor-top-section elementor-element elementor-element-2bdb3ad elementor-section-boxed elementor-section-height-default elementor-section-height-default").find_all("p")
        for x in rows:
            # get span tag that is not inside del tag
            if x.find("span", class_="woocommerce-Price-amount amount") != None and x.find("del") == None:
                # get text from span tag
                self.price = x.find("span", class_="woocommerce-Price-amount amount").text
                # clear text from unnecessary characters
                self.price = self.price.replace("zł", "").replace(" ", "").replace(",", ".")
                # clear all non ascii characters
                self.price = self.price.encode("ascii", "ignore").decode()
                break

class TO_JSON:
    def __init__(self):
        # generate json file name with timestamp
        self.name = "generated_files/products-" + datetime.datetime.now().strftime("%m-%d-%Y-%H") + ".json"
        self.clear_all_json()
    def save(self, product):
        # save product in json file
        with open(self.name, "a", encoding="utf-8") as file:
            json.dump(product.__dict__, file, indent=4, ensure_ascii=False)
    def clear_all_json(self):
        # clear all json files in generated_files folder
        for file in os.listdir("generated_files"):
            if file.endswith(".json"):
                os.remove(os.path.join("generated_files", file))
        
            
class CSV:
    def __init__(self):
        # generate csv file name with timestamp
        self.name = "generated_files/products-" + datetime.datetime.now().strftime("%m-%d-%Y-%H") + ".csv"
        self.set_header()
        self.clear_all_csv()
        
    def set_header(self):
        with open(self.name, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Link", "Price"])

    def save(self, product):
        # save product on new line in csv file
        with open(self.name, "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([product.title, product.href, product.price])
    def clear_all_csv(self):
        # clear all csv files in generated_files folder
        for file in os.listdir("generated_files"):
            if file.endswith(".csv"):
                os.remove(os.path.join("generated_files", file))
            

def get_all_items(url):
    # Pobieranie strony
    page = requests.get(url)

    # Tworzenie obiektu BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")

    # Search for all products by div class
    products = soup.find_all("div", class_="woocommerce-loop-product__title")
    for x in products:
        product = Product(x.text, x.find("a")["href"])
        product.scrap_price()
        # append product to csv file
        saver.save(product)
        saver_json.save(product)
        
def get_all_pages():
    # Get all pages from main page
    page = requests.get("https://czteryszuflady.pl/sklep/kategorie/pokemon-tcg/page/1/")
    soup = BeautifulSoup(page.content, "html.parser")
    pages = soup.find("ul", class_="page-numbers").find_all("li")
    link_list = []
    link_list.append("https://czteryszuflady.pl/sklep/kategorie/pokemon-tcg/page/1/")
    # extract only html links from pages
    for x in pages:
        if x.find("a") != None:
            # append link to list
            link_list.append(x.find("a")["href"])
    # remove duplicates from list
    link_list = list(dict.fromkeys(link_list))
    
    # itearate over all pages
    for i in link_list:
        get_all_items(i)
    
saver_json = TO_JSON()
saver = CSV()
get_all_pages()