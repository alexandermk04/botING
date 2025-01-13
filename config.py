import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC = os.getenv("ANTHROPIC")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

PLAN_PATH = os.getenv("PLAN_PATH")

SENDER = os.getenv("SENDER")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER = os.getenv("RECEIVER")
