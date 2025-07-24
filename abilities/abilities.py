from bot.basic_functions import send_message, send_file
from abilities.exams import ExamScraper
from abilities.mensa import MensaScraper
from config import PLAN_PATH

class BaseAbility:
    def __init__(self, recipient) -> None:
        self.recipient = recipient

    async def execute(self, **kwargs):
        raise NotImplementedError("This method should be overridden by subclasses.")

class ShowHelp(BaseAbility):
    def __init__(self, recipient):
        super().__init__(recipient)

    async def show_help(self):
        """Show help message with available commands and features."""
        await send_message(self.recipient, f"""
Ein Fehler ist aufgetreten. Bitte versuche es später erneut.
""")
        return "Help message sent."

class ExamAvailability(BaseAbility):
    def __init__(self, recipient):
        super().__init__(recipient)

    async def show_exam_availability(self):
        """Informs the user about whether the exam dates are available."""

        try:
            scraper = ExamScraper()
            if scraper.exams_available():
                await send_message(self.recipient, "Prüfungen sind verfügbar!")
            else:
                await send_message(self.recipient, "Keine Prüfungen verfügbar!")
            
            return "Exam availability message sent."
        except:
            await send_message(self.recipient, "Fehler beim Abrufen der Prüfungen.")

            return "Error retrieving exam availability."

class ExamDates(BaseAbility):
    def __init__(self, recipient):
        super().__init__(recipient)

    async def gather_exam_dates(self):
        """Retrieves all the available exam dates."""
        try:
            scraper = ExamScraper()
            return scraper.get_exams()
        except:
            return "Error retrieving exam dates."

class MensaPlan(BaseAbility):
    def __init__(self, recipient):
        super().__init__(recipient)

    async def send_meals(self, day: str, mensa_id: str):
        """Sends the meals available at the given day in the Mensa to the user.
        Args:
            day (str): The day for which to retrieve meals, must be either "heute" or "morgen".
            mensa_id (str): The ID of the Mensa location to retrieve meals from, for example "158".
            Popular IDs are:
                "TUHH": "158",
                "Finkenau": "164",
                "Mensa Philturm, Standort Staatsbibliothek": "154",
                "Mensa Studierendenhaus, Standort Staatsbibliothek": "137"
            You can nonetheless use an ID provided by the user.
        """
        try:
            meals = MensaScraper(day, mensa_id=mensa_id).get_meals()
            await send_message(self.recipient, meals)
            return f"Meals for {day} sent."
        except:
            await send_message(self.recipient, "Fehler beim Abrufen der Mensa-Speisekarte.")
            return "Error retrieving today's meals."

class CampusPlan(BaseAbility):
    def __init__(self, recipient):
        super().__init__(recipient)

    async def send_campus_plan(self):
        try:
            await send_file(self.recipient, "Hier ist der Campusplan:", PLAN_PATH)
            return "Campus plan sent."
        except:
            await send_message(self.recipient, "Fehler beim Senden des Campusplans.")
            return "Error sending campus plan."
