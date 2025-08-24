"""
Agent which demonstrates Human Input tool
"""

import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Human Input")


# Define the agent
@fast.agent(
    instruction="An AI agent that assists with basic tasks. Request Human Input when needed.",
    servers=["random_number_generator"],
    human_input=True,
)
async def main() -> None:
    async with fast.run() as agent:
        # this usually causes the LLM to request the Human Input Tool
        await agent("ask the user what they want")
        # await agent.prompt(default_prompt="STOP")


if __name__ == "__main__":
    asyncio.run(main())
