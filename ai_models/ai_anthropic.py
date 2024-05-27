import anthropic
import logging

from config import ANTHROPIC
from bot.basic_functions import send_message

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = "Respond the shortest way possible."

def anthropic_chat(user_message: str):
    client = anthropic.Anthropic(api_key=ANTHROPIC)

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        temperature=0.5,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )
    logger.info(f"Bot says: {response.content[0].text}")
    return response.content[0].text

def prompt_chat(prompt: str, user_message: str):
    client = anthropic.Anthropic(api_key=ANTHROPIC)

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        temperature=0.5,
        system=prompt + SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )
    logger.info(f"Bot says: {response.content[0].text}")
    return response.content[0].text

async def ai_answer(recipient, user_message):
    response = anthropic_chat(user_message)
    await send_message(recipient, response)

