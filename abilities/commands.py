
from basic_functions import send_message, send_file
from abilities.exams import ExamScraper

class BaseCommand:
    def __init__(self) -> None:
        pass

    async def execute(self, recipient):
        pass


class ExamAvailability(BaseCommand):
    async def execute(self, recipient):
        scraper = ExamScraper()
        if scraper.exams_available():
            await send_message(recipient, "Prüfungen sind verfügbar!")
        else:
            await send_message(recipient, "Keine Prüfungen verfügbar!")
