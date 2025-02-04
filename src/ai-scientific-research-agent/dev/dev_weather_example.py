# First we initialize the model we want to use.
# llm = ChatOllama(model="llama3-groq-tool-use:8b").bind_tools(tools=tools)
from typing import Literal

from langchain_core.tools import tool
from langchain_ollama.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


def run_test_workflow():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [get_weather]

    config = {"configurable": {"thread_id": 1}}

    checkpointer = MemorySaver()

    from langgraph.prebuilt import create_react_agent

    graph = create_react_agent(model, tools=tools, checkpointer=checkpointer)

    while True:
        user_input = input("User: ")
        inputs = {"messages": [("user", user_input)]}
        print_stream(graph.stream(inputs, config, stream_mode="values"))
