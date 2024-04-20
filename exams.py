from bs4 import BeautifulSoup
from rank_bm25 import BM25Okapi
import numpy as np
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
    
    def find_exam(self, message):
        relevant = self.find_relevant(message)
        if relevant:
            most_relevant = self.most_relevant(relevant, message)
            extracted_date = most_relevant[1].find("td", class_="middle")
            return most_relevant[0].text, extracted_date.text
        return None
    
    def find_relevant(self, message):
        chunks = re.sub(r'\b(?:Prüfung|Termin|Datum)\b', '', message).split(" ")
        names, dates = self.extract_info()
        relevant = []

        for chunk in chunks:
            for i, name in enumerate(names):
                if chunk in name.text.lower():
                    relevant.append((name, dates[i]))
                    print(name.text)
        return relevant
    
    def most_relevant(self, relevant, message):
        tokenized_names = [name.text.lower().split(" ") for name, _ in relevant]
        bm25 = BM25Okapi(tokenized_names)
        scores = bm25.get_scores(message.lower().split(" "))
        index_max = np.argmax(scores)

        return relevant[index_max]

    
    def extract_info(self):
        if self.content:
            table = self.content.find("table", class_="prtermine")
            names = table.find_all("tr", class_="titleline")
            dates = table.find_all("tr", class_="dataline")
            return names, dates
        return None
    
    
    
    