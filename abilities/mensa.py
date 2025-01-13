from datetime import datetime

from bs4 import BeautifulSoup
import requests
import re


class MensaScraper:
    page_to_scrape = None
    soup: BeautifulSoup = None
    day: str
    location_id: str
    style: str

    def __init__(self, day="heute", location_id="158", style="md"):
        self.day = day
        self.location_id = location_id
        self.style = style
        if self.day == "morgen":
            self.page_to_scrape = requests.get("https://www.stwhh.de/speiseplan?t=next_day")
        else:
            self.page_to_scrape = requests.get("https://www.stwhh.de/speiseplan?t=today")
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
        response = self.format_meals(meals)
        return response

    def find_correct_location(self):
        rows = self.soup.find_all("div", class_="container-fluid px-0 tx-epwerkmenu-menu-location-container")
        for row in rows:
            if row.get("data-location-id") == self.location_id:
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

        result = {"name": self.clean_meal_name(meal_name), "price": meal_price, "vegan": False}

        # Search for vegan tooltip
        icon_tooltips = meal_block.findAll("span", class_="singlemeal__icontooltip")
        for tooltip in icon_tooltips:
            text = tooltip.get('title')
            if text:
                if "vegan" in text.lower():
                    result["vegan"] = True

        return result
    
    def clean_meal_name(self, meal_name):
        return re.sub(r'\s*\([^)]*\)', '', meal_name)
    
    def format_meals(self, meals: list[dict]) -> str:
        if self.style == "md":
            return self.format_meals_md(meals)
        elif self.style == "html":
            return self.format_meals_html(meals)
        else:
            raise ValueError("Invalid style")
    
    def format_meals_md(self, meals: list[dict]) -> str:
        start_message = f"Hier sind die Gerichte für {self.day}:\n\n"
        meal_messages = [self.format_single_meal_md(meal) for meal in meals]
        response = start_message + "\n".join(meal_messages)

        return response
    
    def format_meals_html(self, meals: list[dict]) -> str:
        start_message = f"<h1>Hier sind die Gerichte für {self.day}:</h1>"
        meal_message = "".join([self.format_single_meal_html(meal) for meal in meals])
        response = self.email_body(start_message + meal_message)

        return response

    def format_single_meal_md(self, meal: dict) -> str:
        if meal["price"] == "0,85 €":
            return f"**Pasta & Gemüsebar ({meal['price']} / 100g):**\n{meal['name']}\n"
        else:
            return f"**{meal['name']}**\n{meal['price']}\n"
        
    def format_single_meal_html(self, meal: dict) -> str:
        if meal["name"] == "Dummy Hauptkomponente":
            return ""
        if meal["price"] == "0,85 €":
            text = f"<p><strong>{meal['name']}</strong><br>Pasta & Gemüsebar ({meal['price']} / 100g):"
        else:
            text =  f"<p><strong>{meal['name']}</strong><br>{meal['price']}"
        if meal["vegan"]:
            text += "<br><strong>Vegan</strong>"

        # Close the paragraph
        text += "</p>"
        return text
        
    def email_body(self, content: str):
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                    }}
                    p {{
                        margin: 10px 0;
                    }}
                    strong {{
                        color: #007BFF;  /* Example: Blue for emphasis */
                    }}
                </style>
            </head>
            <body>
                {content}
            </body>
        </html>
        """
        return html_body
