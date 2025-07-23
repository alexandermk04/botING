from bs4 import BeautifulSoup
from rank_bm25 import BM25Okapi
import requests
import re

SEMESTER = "SOMMERSEMESTER"

class ExamScraper:
    page_to_scrape = None
    content: BeautifulSoup = None

    def __init__(self):
        self.page_to_scrape = requests.get("https://intranet.tuhh.de/stud/pruefung/index.php?Lang=de")
        if self.page_to_scrape:
            self.content = BeautifulSoup(self.page_to_scrape.text, "html.parser")
        else:
            print("Error while fetching page")

    def exams_available(self):
        if self.content:
            semester = self.content.find("h2")
            if SEMESTER.lower() in semester.text.lower():
                return True
        return False
    
    def get_exams(self):
        names, dates = self.extract_info()

        exams: dict[str, str] = {}
        for name, date in zip(names, dates):
            extracted_date = date.find("td", class_="middle")
            if extracted_date:
                exams[name.text.strip()] = extracted_date.text.strip()
        return exams

    
    def extract_info(self):
        if self.content:
            table = self.content.find("table", class_="prtermine")
            names = table.find_all("tr", class_="titleline")
            dates = table.find_all("tr", class_="dataline")

            return names, dates 
        return None
    
    
    
    