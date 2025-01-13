import discord
import logging


from config import DISCORD_TOKEN
from message_handler import MessageHandler

logger = logging.getLogger(__name__)

async def run_discord_bot():
    
    intents = discord.Intents.default()
    intents.message_content = True
    
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        logger.info(f"{client.user} is now running!")
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await MessageHandler(message).answer()

    await client.start(DISCORD_TOKEN)

    
