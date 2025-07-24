import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC = os.getenv("ANTHROPIC")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

PLAN_PATH = os.getenv("PLAN_PATH")

PAYPAL = os.getenv("PAYPAL")

SENDER = os.getenv("SENDER")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER = os.getenv("RECEIVER")

FIREBASE_PATH = os.getenv("FIREBASE_PATH")
