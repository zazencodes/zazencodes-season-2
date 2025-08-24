import asyncio

from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Furigana Troll")


@fast.agent(
    instruction="Always respond in a mix of Furigana and english. Every other word should be japanese"
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
