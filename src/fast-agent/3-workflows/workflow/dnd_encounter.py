"""
Agent which demonstrates Human Input tool
"""

import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("dnd encounter")


# Define the agent
@fast.agent(
    servers=["random_number_generator"],
)
async def main() -> None:
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
