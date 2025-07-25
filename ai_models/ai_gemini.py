import logging

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from google.genai.types import Content, Part

from dto import Conversation

from abilities.abilities import (
    BaseAbility,
    ShowHelp,
    ExamAvailability,
    ExamDates,
    MensaPlan,
    CampusPlan,
)
from abilities.user_memory import UserMemory

APP_NAME = "BotING"
MODEL_NAME = "gemini-2.0-flash"
AGENT_SESSION = "agent_session"

def gather_abilities(user_id, recipient) -> list[BaseAbility]:
    memory = UserMemory(user_id=user_id)

    return [
        ShowHelp(recipient).show_help,
        ExamAvailability(recipient).show_exam_availability,
        ExamDates(recipient).gather_exam_dates,
        MensaPlan(recipient).send_meals,
        CampusPlan(recipient).send_campus_plan,
        memory.store_user_info,
    ]

async def create_agent_runner(recipient, user_id: str) -> Runner:
    abilities = gather_abilities(user_id=user_id, recipient=recipient)

    user_info = UserMemory(user_id=user_id).get_user_info()

    agent = LlmAgent(
        model=MODEL_NAME,
        name="function_call_agent",
        description="Executes functions based on user input.",
        instruction=f"""You are BotING, a helpful discord assistant, supporting students in their daily life the the Hamburg University of Technology (TUHH).
        You can use your functions to send them information, as well as communicate with them.
        Generally assume that the user speaks German.
        You can use the 'get_user_info' function to fetch information from past conversations.
        Using the 'store_user_info' function, you should store information about the user for future use.
        If asked about food ("Essen"), assume that the user wants to know the meals available **today**.
        
        This is additional information about the user:
        {user_info}
        """,
        tools=abilities,
    )
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=AGENT_SESSION,
    )

    runner = Runner(app_name=APP_NAME, agent=agent, session_service=session_service)
    return runner

async def create_answer(conversation: Conversation, recipient) -> str | None:
    user_id = conversation.message.user_id
    runner = await create_agent_runner(recipient, user_id=user_id)

    history_parts = [
        Part(text=f"{msg.author}: {msg.content}") for msg in conversation.history
    ]
    message_part = Part(text=f"{conversation.message.author}: {conversation.message.content}")

    history_parts.append(message_part)

    content = Content(role='user', parts=history_parts)

    logger.info(content)

    async for event in runner.run_async(user_id=user_id, session_id=AGENT_SESSION, new_message=content):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            return final_response
        
    return None