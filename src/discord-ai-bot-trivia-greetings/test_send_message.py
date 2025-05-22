import asyncio
import logging
import os

import discord
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("TestClient")

load_dotenv()

CHANNEL_ID = 87329748324782394723  # Replace with your ID


class TestClient(discord.Client):
    def __init__(self, channel_id):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.target_channel_id = int(channel_id)

    async def setup_hook(self):
        logger.info("Setting up test client...")
        self.loop.create_task(self.simulate_message())

    async def on_ready(self):
        logger.info(f"Test client logged in as {self.user}")
        logger.info(f"Test client is in {len(self.guilds)} guilds")
        for guild in self.guilds:
            logger.info(f"- {guild.name} (id: {guild.id})")
            for channel in guild.channels:
                logger.info(f"  > {channel.name} (id: {channel.id})")

    async def simulate_message(self):
        logger.info("Waiting for client to be ready...")
        await self.wait_until_ready()

        try:
            # Find the channel
            channel = self.get_channel(self.target_channel_id)
            if not channel:
                logger.error(f"Could not find channel with ID {self.target_channel_id}")
                await self.close()
                return

            logger.info(f"Found channel: {channel.name} (id: {channel.id})")

            # Send a test message
            logger.info("Sending test message...")
            test_message = await channel.send(
                "This is a test message from the test client!"
            )
            logger.info(f"Test message sent with ID: {test_message.id}")

            # Wait a moment to see if the main bot responds
            logger.info("Waiting for potential bot response...")
            await asyncio.sleep(5)

            logger.info("Test completed!")
            await self.close()

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}", exc_info=True)
            await self.close()


async def main():
    # Verify environment variables
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if not bot_token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        return

    # Create and run test client
    test_client = TestClient(CHANNEL_ID)
    try:
        logger.info("Starting test client...")
        await test_client.start(bot_token)
    except Exception as e:
        logger.error(f"Failed to run test: {str(e)}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
