import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC = os.getenv("ANTHROPIC")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

PLAN_PATH = os.getenv("PLAN_PATH")
