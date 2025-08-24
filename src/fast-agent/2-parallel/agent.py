import asyncio

from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Model Comparison")

PROMPT = (
    # "What year did Hokusai start and complete his 100 views of Mt. Fuji collection?"
    "What are Mozarts most celebrated pieces?"
)


@fast.agent("gpt_5", model="openai.gpt-5")
@fast.agent("gpt_5_mini", model="openai.gpt-5-mini")
@fast.agent("gpt_5_nano", model="openai.gpt-5-nano")
@fast.agent("sonnet", model="anthropic.claude-sonnet-4-0")
@fast.agent("gemma3_4b", model="generic.gemma3:4b")
@fast.agent("deepseek", model="generic.deepseek-r1:1.5b")
@fast.agent("qwen", model="generic.qwen3:0.6b")
@fast.parallel(
    name="compare",
    fan_out=[
        "gpt_5",
        "sonnet",
        "gemma3_4b",
        "gpt_5_mini",
        "gpt_5_nano",
        "deepseek",
        "qwen",
    ],
)
async def main():
    async with fast.run() as agent:
        res = await agent.compare(PROMPT)
        print(res)
        await agent.gpt_5_mini.send(
            f"Sythesize these responses into a simple output table compaing the differnet models: {res}"
        )


if __name__ == "__main__":
    asyncio.run(main())
