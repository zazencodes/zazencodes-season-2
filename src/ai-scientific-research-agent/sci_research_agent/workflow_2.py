import logging
from io import BytesIO
from typing import Annotated, Literal

# from langchain_anthropic import ChatAnthropic
# from langchain_ollama.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from PIL import Image
from typing_extensions import TypedDict

from .arxiv import arxiv_search
from .latex import render_latex_pdf
from .pdf import read_pdf

# Setup module logger
logger = logging.getLogger(__name__)

INITIAL_PROMPT = """
You are an expert researcher in the fields of physics, mathematics,
computer science, quantitative biology, quantitative finance, statistics,
electrical engineering and systems science, and economics.

You are going to analyze recent research papers in one of these fields in
order to identify promising new research directions and then write a new
research paper.

To start with, have a conversation with me in order to figure out what topic
to research. Then tell me about some recently published papers with that topic.
Once I've decided which paper I'm interested in, go ahead and read it in order
to understand the research that was done and the outcomes.

Pay particular attention to the ideas for future research and think carefully
about them, then come up with a few ideas. Let me know what they are and I'll
decide what one you should write a paper about.

Finally, I'll ask you to go ahead and write the paper. Make sure that you
include mathematical equations in the paper. Once it's complete, you should
render it as a LaTeX PDF.
"""


class State(TypedDict):
    messages: Annotated[list, add_messages]


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        logger.info(f"Message received: {message.content[:200]}...")
        message.pretty_print()


def run_workflow():
    logger.info("Initializing workflow")

    tools = [arxiv_search, read_pdf, render_latex_pdf]
    tool_node = ToolNode(tools)

    model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
    # model = ChatAnthropic(model="claude-3-5-sonnet-20241022").bind_tools(tools)
    # model = ChatOllama(model="llama3-groq-tool-use:8b").bind_tools(tools)

    logger.info(f"Initialized model and loaded {len(tools)} tools")

    # Define the function that determines whether to continue or not
    def should_continue(state: State) -> Literal["tools", END]:
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END

    # Define the function that calls the model
    def call_model(state: State):
        messages = state["messages"]
        response = model.invoke(messages)
        return {"messages": [response]}

    config = {"configurable": {"thread_id": 1}}
    logger.info(f"Set configuration: {config}")

    workflow = StateGraph(State)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")

    checkpointer = MemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)

    Image.open(BytesIO(graph.get_graph().draw_mermaid_png())).show()

    logger.info("Created workflow agent graph")

    logger.info("Starting conversation with initial prompt")
    inputs = {"messages": [("user", INITIAL_PROMPT)]}
    print_stream(graph.stream(inputs, config, stream_mode="values"))

    # Start chatbot
    logger.info("Entering interactive chat loop")
    while True:
        user_input = input("User: ")
        logger.info(f"Received user input: {user_input[:200]}...")
        inputs = {"messages": [("user", user_input)]}
        print_stream(graph.stream(inputs, config, stream_mode="values"))
