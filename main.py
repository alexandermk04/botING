import bot.bot as bot
from abilities.newsletter import Newsletter
import schedule
import asyncio

def init_newsletter():
    newsletter_instance = Newsletter()
    newsletter_instance.send()
    print("Successfully sent newsletter")

schedule.every().day.at("20:00").do(init_newsletter)

async def run_schedule():
    """Run the schedule in an async loop."""
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)  # Use asyncio.sleep for non-blocking sleep

async def main():
    """Run the bot and schedule loop concurrently."""
    # Run both the Discord bot and the scheduler in parallel
    await asyncio.gather(
        run_schedule(),
        bot.run_discord_bot()  # Ensure this is an async function
    )

if __name__ == "__main__":
    asyncio.run(main())