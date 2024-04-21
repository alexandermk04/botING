from rank_bm25 import BM25Okapi
import numpy as np

from abilities.commands import ExamAvailability

CHANNELS = ["bot-ing"]

COMMANDS = {"prüfungen": ExamAvailability()}
ABILITIES = []

class MessageHandler:
    username: str
    user_message: str
    channel: str
    type: str
    message = None

    def __init__(self, message):
        self.username = str(message.author)
        self.user_message = str(message.content)
        self.channel = str(message.channel)
        self.message = message

        print(f"{self.username} said {self.user_message} in {self.channel}")

        self.recognize_type()

    def recognize_type(self):
        if self.user_message[0] == "!":
            self.type = "command"
        else:
            self.type = "message"

    async def answer(self):
        if self.channel not in CHANNELS:
            return
        
        if self.type == "command":
            command = self.recognize_command()
            if command:
                return await command.execute(self.message.channel)
        else:
            ability = self.recognize_ability()
            if ability:
                return await ability.execute(self.message.channel)
        
    def recognize_command(self):
        cleaned_message = self.user_message[1:].strip()
        command = COMMANDS.get(cleaned_message)

        return command   
        
    def recognize_ability(self):
        tokenized_abilities = [ability.keywords.split(" ") for ability in ABILITIES]
        bm25 = BM25Okapi(tokenized_abilities)
        scores = bm25.get_scores(self.user_message.lower().split(" "))
        index_max = np.argmax(scores)

        return ABILITIES[index_max]

    

    