from webscraper import MensaScraper
from abilities.exams import ExamScraper

def handle_response(message) -> str:
    p_message = message.lower()

    if "alex" in p_message:
        return "Schluckscheißer!"

    if "essen" in p_message or "menü" in p_message or "gericht" in p_message:
        meals = MensaScraper().get_meals()
        if meals:
            return format_meal(meals)
        else:
            return "Ich konnte leider keine Gerichte finden." 
        
    if "prüfung" in p_message or "klausur" in p_message or "exam" in p_message:
        exams = ExamScraper()
        if exams.exams_available():
            if "termin" in p_message or "datum" in p_message:
                response = exams.find_exam(p_message)
                if response:
                    return f"Die Prüfung **{response[0]}** findet am **{response[1]}** statt."
                else:
                    return "Ich konnte leider keinen passenden Termin finden."
            else:
                return "Es gibt Prüfungstermine für das aktuelle Semester!"
            
        else:
            return "Es gibt noch keine Prüfungstermine für das aktuelle Semester!"
    
    else:
        return "Ich kann dir leider nicht helfen."
    

def format_meal(meals: list[dict]) -> str:
    start_message = "Hier sind die Gerichte für heute:\n\n"
    meal_messages = [format_single_meal(meal) for meal in meals]
    response = start_message + "\n".join(meal_messages)
    return response

def format_single_meal(meal: dict) -> str:
    if meal["price"] == "0,75 €":
        return f"**Pasta & Gemüsebar ({meal['price']} / 100g):**\n{meal['name']}\n"
    else:
        return f"**{meal['name']}**\n{meal['price']}\n"