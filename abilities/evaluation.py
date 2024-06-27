from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import re

WEEK = 6

class DiscordUser():
    tag: str
    group: str
    group_name: str

    def __init__(self, tag: str, group: str, group_name: str):
        self.tag = tag
        self.group = group
        self.group_name = group_name

DISCORD_TO_TAG = {
    "bl3x": DiscordUser("cnm5281", "G7", "BogoSort"),
    "sixseveneight": DiscordUser("cci0492", "G7", "BogoSort"),
    "eagleplay.exe": DiscordUser("cgj4967", "G7", "BogoSort"),
}

def get_week():
    current_date = datetime.now()
    
    # Remember to update as holidays are added
    delta_days = (current_date - datetime(2024, 6, 16)).days
    
    weeks_passed = delta_days // 7

    return str(WEEK + weeks_passed).zfill(2)


class EvaluationScraper:
    
    def __init__(self, user):
        self.discord_user = DISCORD_TO_TAG.get(user)    # potentially add more sophisticated group name determination
        self.week = get_week()
        self.page_to_scrape = requests.get(f"https://oopy.teluapps.com/evals/{self.discord_user.group}/{self.discord_user.group_name}/{self.discord_user.tag}/s{self.week}")
        if self.page_to_scrape:
            self.soup = BeautifulSoup(self.page_to_scrape.text, "html.parser")
        else:
            print("Error fetching page.")

    def get_evaluation(self):
        if not self.soup or not self.discord_user:
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
        response = f"**Evaluation von {self.discord_user.tag} für Aufgabe {self.week}**\n"
        for item in evaluation:
            response += f"- {item}\n"
        response += f"\n**Punkte**: {points}"
        return response
