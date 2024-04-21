import discord

from config import DISCORD_TOKEN, PLAN_PATH
from basic_functions import send_message, send_file
from message_handler import MessageHandler

def run_discord_bot():
    
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await MessageHandler(message).answer()

    client.run(DISCORD_TOKEN)

    
