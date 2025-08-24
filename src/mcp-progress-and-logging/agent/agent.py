import asyncio

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.request_params import RequestParams

# Create the application
fast = FastAgent("fast-agent vegan recipes fetcher")


@fast.agent(
    name="vegan-recipe-fetcher",
    servers=["vegan_recipes_mcp"],
    request_params=RequestParams(
        maxTokens=55000,
    ),
)
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())
