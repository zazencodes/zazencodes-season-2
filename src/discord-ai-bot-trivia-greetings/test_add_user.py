import asyncio
import logging
import os

import discord
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("TestClient")

load_dotenv()


class TestClient(discord.Client):
    def __init__(self):
        # Make sure to enable all intents
        intents = discord.Intents.all()
        super().__init__(intents=intents)

    async def setup_hook(self):
        logger.info("Setting up test client...")
        # Wait a bit before simulating join to ensure bot is fully ready
        self.loop.create_task(self.delayed_simulate_join())

    async def on_ready(self):
        logger.info(f"Test client logged in as {self.user}")
        logger.info(f"Test client is in {len(self.guilds)} guilds")
        for guild in self.guilds:
            logger.info(f"- {guild.name} (id: {guild.id})")

    async def delayed_simulate_join(self):
        # Wait for bot to be fully ready
        await asyncio.sleep(2)
        await self.simulate_member_join()

    async def simulate_member_join(self):
        try:
            # Get the guild
            guild_id = os.getenv("DISCORD_TEST_GUILD_ID")
            if not guild_id:
                logger.error("No guild ID provided")
                await self.close()
                return

            guild = self.get_guild(int(guild_id))
            if not guild:
                logger.error(f"Could not find guild with ID {guild_id}")
                await self.close()
                return

            logger.info(f"Found guild: {guild.name} (id: {guild.id})")

            # Get a random member to use as test subject (not the bot itself)
            members = [m for m in guild.members if not m.bot]
            if not members:
                logger.error("No non-bot members found in guild")
                await self.close()
                return

            test_member = members[0]
            logger.info(f"Using test member: {test_member.name} (id: {test_member.id})")

            # Manually create and dispatch member join event
            logger.info("Dispatching member join event...")
            self.dispatch("member_join", test_member)

            # Wait to see the results
            logger.info("Waiting for bot response...")
            await asyncio.sleep(5)

            logger.info("Test completed!")
            await self.close()

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}", exc_info=True)
            await self.close()

    async def on_member_join(self, member):
        logger.info(f"Member join event detected for {member.name} (id: {member.id})")


async def main():
    logger.warning(
        "This script does what it should, but the bot doesn't pick up the event. So I've been testing manually using my alt account."
    )

    # Verify environment variables
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if not bot_token:
        logger.error("DISCORD_BOT_TOKEN not found in environment variables")
        return

    guild_id = os.getenv("DISCORD_TEST_GUILD_ID")
    if not guild_id:
        guild_id = input("Please enter your guild (server) ID: ")
        os.environ["DISCORD_TEST_GUILD_ID"] = guild_id
        logger.info(f"Using guild ID: {guild_id}")

    # Create and run test client
    client = TestClient()
    try:
        logger.info("Starting test client...")
        await client.start(bot_token)
    except Exception as e:
        logger.error(f"Failed to run test: {str(e)}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
