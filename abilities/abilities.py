from basic_functions import send_message, send_file
from ai_models.phi_3 import prompt_chat, phi_3_answer
from abilities.exams import ExamScraper
from abilities.mensa import MensaScraper
from config import PLAN_PATH

class BaseAbility:
    def __init__(self) -> None:
        pass

    async def execute(self, recipient, **kwargs):
        pass

class Conversation(BaseAbility):
    async def execute(self, recipient, user_message, **kwargs):
        await phi_3_answer(recipient, user_message)

class ExamAvailability(BaseAbility):
    async def execute(self, recipient, **kwargs):
        scraper = ExamScraper()
        if scraper.exams_available():
            await send_message(recipient, "Prüfungen sind verfügbar!")
        else:
            await send_message(recipient, "Keine Prüfungen verfügbar!")

class ExamDates(BaseAbility):
    async def execute(self, recipient, user_message, **kwargs):
        scraper = ExamScraper()
        exams = scraper.find_exam(user_message)

        if exams:
            prompt = "Supply the user with the most relevant exam date as well as the name of the following:"
            exams_string = "\n".join([f"{exam[0]} at {exam[1]}" for exam in exams])
            response = prompt_chat(prompt + exams_string, user_message)
            await send_message(recipient, response)

class MealsToday(BaseAbility):

    async def execute(self, recipient, **kwargs):
        meals = MensaScraper("heute").get_meals()
        await send_message(recipient, meals)

class MealsTomorrow(BaseAbility):

    async def execute(self, recipient, **kwargs):
        meals = MensaScraper("morgen").get_meals()
        await send_message(recipient, meals)

class Plan(BaseAbility):
    async def execute(self, recipient, user_message, **kwargs):
        await send_file(recipient, "Hier ist der Campusplan:", PLAN_PATH)

ABILITIES = {"prüfungen verfügbar": ExamAvailability(),
             "prüfungstermine": ExamDates(),
             "mensa heute": MealsToday(),
             "mensa morgen": MealsTomorrow(),
             "conversation": Conversation(),
             "campus": Plan()}