import logging
import datetime

from abilities.abilities import ShowHelp
from bot.basic_functions import send_message
from ai_models.ai_gemini import create_answer
from dto import Conversation, Message

logger = logging.getLogger(__name__)

HISTORY_LENGTH = 5
TIME_CUTOFF_MINUTES = 2

CHANNELS = ["bot-ing", "Direct Message with Unknown User"]

class MessageHandler:
    username: str
    user_message: str
    channel: str
    type: str
    message = None

    def __init__(self, message):
        self.username = str(message.author)
        self.user_message = str(message.content)[:200]
        self.channel = str(message.channel)
        self.message = message

        logger.info(f"{self.username} said {self.user_message} in {self.channel}")

    async def answer(self):
        if self.channel not in CHANNELS:
            logger.info(f"{self.channel} not allowed.")
            return
        
        try:
            conversation = await self.construct_conversation()
            answer = await create_answer(conversation, recipient=self.message.channel)

            if answer is not None:
                return await send_message(self.message.channel, answer)
        except Exception as e:
            logger.error(f"Error in AI response: {e}")
        return await ShowHelp(self.message.channel).show_help()
    
    async def construct_conversation(self) -> Conversation:
        message = Message(
            content=self.user_message,
            author=self.username
        )

        cutoff_time = self.message.created_at - datetime.timedelta(minutes=TIME_CUTOFF_MINUTES)

        history_msg = []
        async for msg in self.message.channel.history(limit=HISTORY_LENGTH, before=self.message):
            if msg.created_at > cutoff_time:
                history_msg.append(msg)

        history_msg.reverse()

        history = [Message(content=msg.content, author=msg.author.name) for msg in history_msg]

        return Conversation(
            message=message,
            history=history
        )
    