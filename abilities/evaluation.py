from bs4 import BeautifulSoup
import requests
import re

WEEK = "s03"

GROUP = "G7"

GROUP_NAME = "BogoSort"

DISCORD_TO_TAG = {
    "bl3x": "cnm5281",
    "sixseveneight": "cci0492",
}

# !! Implement API call instead of scraping the page

class EvaluationScraper:
    
    def __init__(self, user):
        self.discord_user = DISCORD_TO_TAG.get(user)
        # potentially add more sophisticated group name determination
        self.page_to_scrape = requests.get(f"https://oopy.teluapps.com/evals/{GROUP}/{GROUP_NAME}/{self.discord_user}/{WEEK}")
        if self.page_to_scrape:
            self.soup = BeautifulSoup(self.page_to_scrape.text, "html.parser")
        else:
            print("Error fetching page.")

    def get_evaluation(self):
        if not self.soup:
            return None
        evaluation, points = self.extract_evaluation()
        response = self.format_evaluation(evaluation, points)
        return response
        
    def extract_evaluation(self):
        evaluation = self.soup.find("ol")
        extracted_evaluation = evaluation.find_all("li")
        points = self.soup.find("p")
        return [item.text for item in extracted_evaluation], points.text
    
    def format_evaluation(self, evaluation, points):
        response = f"**Evaluation von {self.discord_user} für Aufgabe {WEEK.upper()}**\n"
        for item in evaluation:
            response += f"- {item}\n"
        response += f"\n**Punkte**: {points}"
        return response