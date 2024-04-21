import discord

async def send_message(recipient, message):
    try:
        await recipient.send(message)
    except Exception as e:
        print(e)

async def send_file(recipient, message, file_path):
    try: 
        with open(file_path, 'rb') as f:
            await recipient.send(message, file=discord.File(f))
    except Exception as e:
        print(e)


