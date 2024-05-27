from bot.basic_functions import send_message, send_file
from ai_models.ai_anthropic import ai_answer
from abilities.exams import ExamScraper
from abilities.mensa import MensaScraper
from abilities.evaluation import EvaluationScraper
from config import PLAN_PATH

class BaseAbility:
    def __init__(self) -> None:
        pass

    async def execute(self, recipient, **kwargs):
        pass

class Conversation(BaseAbility):
    async def execute(self, recipient, user_message, **kwargs):
        await ai_answer(recipient, user_message)

class ShowHelp(BaseAbility):
    async def execute(self, recipient, **kwargs):
        await send_message(recipient, "Probiere einen der folgenden Commands aus:\n"
                                      "!prüfungen verfügbar\n"
                                      "!prüfungstermine\n"
                                      "!mensa heute\n"
                                      "!mensa morgen\n"
                                      "!campus")

class ExamAvailability(BaseAbility):
    async def execute(self, recipient, **kwargs):
        try:
            scraper = ExamScraper()
            if scraper.exams_available():
                await send_message(recipient, "Prüfungen sind verfügbar!")
            else:
                await send_message(recipient, "Keine Prüfungen verfügbar!")
        except:
            await send_message(recipient, "Fehler beim Abrufen der Prüfungen.")

class ExamDates(BaseAbility):
    async def execute(self, recipient, user_message, **kwargs):
        try:
            scraper = ExamScraper()
            exams = scraper.find_exam(user_message)

            if exams:
                prompt = "Supply the user with the most relevant exam date as well as the name of the following:"
                exams_string = "\n".join([f"{exam[0]} at {exam[1]}" for exam in exams])
                #response = prompt_chat(prompt + exams_string, user_message)
                await send_message(recipient, exams_string)
        except:
            await send_message(recipient, "Fehler beim Abrufen der Prüfungstermine.")

class OOPEvaluation(BaseAbility):
    async def execute(self, recipient, username, **kwargs):
        try:
            await send_message(recipient, f"Suche nach Evaluation für {username}. Dies kann etwas dauern...")
            response = EvaluationScraper(username).get_evaluation()
            await send_message(recipient, response)
        except:
            await send_message(recipient, "Fehler bei der Evaluationssuche.")

class MealsToday(BaseAbility):

    async def execute(self, recipient, **kwargs):
        try:
            meals = MensaScraper("heute").get_meals()
            await send_message(recipient, meals)
        except:
            await send_message(recipient, "Fehler beim Abrufen der Mensa-Speisekarte.")

class MealsTomorrow(BaseAbility):

    async def execute(self, recipient, **kwargs):
        try:
            meals = MensaScraper("morgen").get_meals()
            await send_message(recipient, meals)
        except:
            await send_message(recipient, "Fehler beim Abrufen der Mensa-Speisekarte.")

class Plan(BaseAbility):
    async def execute(self, recipient, **kwargs):
        try:
            await send_file(recipient, "Hier ist der Campusplan:", PLAN_PATH)
        except:
            await send_message(recipient, "Fehler beim Senden des Campusplans.")

ABILITIES = {"prüfungen verfügbar": ExamAvailability(),
             "prüfungstermine": ExamDates(),
             "oop": OOPEvaluation(),
             "mensa heute": MealsToday(),
             "mensa morgen": MealsTomorrow(),
             "conversation": Conversation(),
             "campus": Plan()}