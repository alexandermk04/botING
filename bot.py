import discord
import responses

from config import DISCORD_TOKEN, PLAN_PATH


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

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
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said {user_message} in {channel}")

        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            if channel == "bot-ing":
                if user_message.lower() == "plan":
                    await send_file(message.channel, PLAN_PATH)
                else:
                    await send_message(message, user_message, is_private=False)

    client.run(DISCORD_TOKEN)

async def send_file(channel, file_path):
        with open(file_path, 'rb') as f:
            await channel.send("Hier ist der Gebäudeplan:\n", file=discord.File(f))


    
