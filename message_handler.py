from rank_bm25 import BM25Okapi
import numpy as np

from abilities.abilities import ABILITIES
from ai_anthropic import ai_answer, prompt_chat

CHANNELS = ["bot-ing", "Direct Message with Unknown User"]

INTENT_PROMPT = f"""You're an assistant trying to supply the most relevant information to the user.
                You can execute the following functions:
                {', '.join(ABILITIES.keys())}
                Only reply with the name of the function that is most relevant to the user's message or simply 'None'."""

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
            print(f"{self.channel} not allowed.")
            return
        
        if self.type == "command":
            command = self.recognize_command()
            if command:
                return await command.execute(recipient=self.message.channel)
        else:
            ability = self.recognize_ability()
            if ability:
                return await ability.execute(recipient=self.message.channel,
                                              user_message=self.user_message)
            else:
                return await ai_answer(self.message.channel, self.user_message)
        
    def recognize_command(self):
        cleaned_message = self.user_message[1:].strip()
        command = ABILITIES.get(cleaned_message)

        return command   
        
    def recognize_ability(self):
        response = prompt_chat(INTENT_PROMPT, self.user_message)
        if response == "None":
            return None
        else:
            try:
                return ABILITIES.get(response)
            except KeyError as e:
                print(e)
                return None

    

    