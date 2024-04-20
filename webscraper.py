from bs4 import BeautifulSoup
import requests
import re

class MensaScraper:
    page_to_scrape = None
    soup: BeautifulSoup = None

    def __init__(self):
        self.page_to_scrape = requests.get("https://www.stwhh.de/speiseplan?t=today#c19095")
        if self.page_to_scrape:
            self.soup = BeautifulSoup(self.page_to_scrape.text, "html.parser")
        else:
            print("Error while fetching page")

    def get_meals(self):
        if not self.soup:
            return None
        location_row = self.find_correct_location()
        meals_blocks = self.extract_meals(location_row)
        meals = []
        for meal_block in meals_blocks:
            meal_info = self.extract_meal_info(meal_block)
            meals.append(meal_info)
        return meals

    def find_correct_location(self):
        rows = self.soup.find_all("div", class_="container-fluid px-0 tx-epwerkmenu-menu-location-container")
        for row in rows:
            if row.get("data-location-id") == "158":
                return row

    def extract_meals(self, row):
        meals_blocks = row.findAll("div", class_="singlemeal")
        return meals_blocks

    def extract_meal_info(self, meal_block):
        meal_name_element = meal_block.find("h5", class_="singlemeal__headline singlemeal__headline--")
        if meal_name_element:
            meal_name = meal_name_element.text.strip()
        else:
            meal_name = "Unbekannt"

        meal_prices = meal_block.findAll("dd", class_="dlist__item")
        meal_price = "Unbekannt"

        for price in meal_prices:
            if "Studierende" in price.text:
                price_span = price.find("span", class_="singlemeal__info--semibold")
                if price_span:
                    meal_price = price_span.text.strip()

        return {"name": self.clean_meal_name(meal_name), "price": meal_price}
    
    def clean_meal_name(self, meal_name):
        return re.sub(r'\s*\([^)]*\)', '', meal_name)