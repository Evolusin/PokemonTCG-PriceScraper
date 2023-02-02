import datetime
import json
import os

import requests
from bs4 import BeautifulSoup


class Producter:
    def __init__(self, title, href):
        self.title = title
        self.href = href

    def scrap_price(self):
        page = requests.get(self.href)
        soup = BeautifulSoup(page.content, "html.parser")
        # Search for bdi tag inside of section class but ignore if span class is inside del tag and look for the next bdi tag
        # iterate over p class "price" inside of section class
        rows = soup.find(
            "section",
            class_=(
                "elementor-section elementor-top-section elementor-element"
                " elementor-element-2bdb3ad elementor-section-boxed"
                " elementor-section-height-default"
                " elementor-section-height-default"
            ),
        ).find_all("p")
        # print(rows[0])
        for x in rows:
            del_tag = x.find("del")
            if del_tag is not None:
                self.price = x.find_all("bdi")[1].text
            else:
                span_tag = x.find(
                    "span", class_="woocommerce-Price-amount amount"
                )
                if span_tag is not None and del_tag is None:
                    if "Poprzednia najniższa cena" not in x.text:
                        self.price = span_tag.text
                        break

        self.price = (
            self.price.replace("zł", "").replace(" ", "").replace(",", ".")
        )
        self.price = self.price.encode("ascii", "ignore").decode()

    def return_json(self):
        return self.__dict__


class TO_JSON:
    def __init__(self):
        # generate json file name with timestamp
        self.name = (
            "generated_files/products-"
            + datetime.datetime.now().strftime("%m-%d-%Y-%H-%M")
            + ".json"
        )

    def save(self, product):
        if not os.path.exists(self.name):
            with open(self.name, "w", encoding="utf-8") as file:
                file.write("[\n")
                json.dump(product, file, indent=4, ensure_ascii=False)
                file.write("\n]")
        else:
            with open(self.name, "r", encoding="utf-8") as file:
                data = json.load(file)
                data.append(product)
            with open(self.name, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

    def clear_all_json(self):
        # clear all json files in generated_files folder
        for file in os.listdir("generated_files"):
            if file.endswith(".json"):
                os.remove(os.path.join("generated_files", file))

    def add_date_to_json(self):
        # add date to all json dictionaries
        with open(self.name, "r", encoding="utf-8") as file:
            data = json.load(file)
            for x in data:
                x["date"] = datetime.datetime.now().strftime("%m-%d-%Y-%H:%M:%S")
        with open(self.name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def get_all_items(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    # Search for all products by div class
    products = soup.find_all("div", class_="woocommerce-loop-product__title")
    for x in products:
        product = Producter(x.text, x.find("a")["href"])
        product.scrap_price()
        # append product to json file
        product = product.return_json()
        saver_json.save(product)


def get_all_pages():
    # Get all pages from main page
    page = requests.get(
        "https://czteryszuflady.pl/sklep/kategorie/pokemon-tcg/page/1/"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    pages = soup.find("ul", class_="page-numbers").find_all("li")
    link_list = []
    link_list.append(
        "https://czteryszuflady.pl/sklep/kategorie/pokemon-tcg/page/1/"
    )
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
get_all_pages()
saver_json.add_date_to_json()
