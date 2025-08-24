import asyncio

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.request_params import RequestParams

# Create the application
fast = FastAgent("fast-agent plotter")


@fast.agent(
    name="plotter",
    servers=["quick_plot_csv"],
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
