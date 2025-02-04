import xml.etree.ElementTree as ET
from io import BytesIO
from typing import Annotated, Literal

import requests
from langchain_core.tools import tool
from langchain_ollama.chat_models import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt
from PIL import Image
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages]


def run_research_workflow():
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "1"}}
    tools = [arxiv_search, human_assistance]

    # llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools=tools)
    llm = ChatOllama(model="llama3-groq-tool-use:8b").bind_tools(tools=tools)

    tool_node = ToolNode(tools=tools)

    def welcome(state: State):
        welcome_message = (
            "My job is to write you a research paper. Let's start by finding a good topic "
            "to write about. Do you have any ideas? If not, that's fine - I can help with "
            "that too!"
        )
        return {"messages": [{"role": "assistant", "content": welcome_message}]}

    def chatbot(state: State):
        print("inside chatbot")
        message = llm.invoke(state["messages"])
        assert len(message.tool_calls) <= 1  # Disable parallel tool computing
        return {"messages": [message]}

    def human_review_node(state) -> Command[Literal["chatbot", "tools"]]:
        print("inside human_review_node")
        interrupt({})
        return Command(goto="tools")

    def route_after_llm(state) -> Literal[END, "human_review_node"]:
        if len(state["messages"][-1].tool_calls) == 0:
            return END
        else:
            return "human_review_node"

    graph_builder = StateGraph(State)

    graph_builder.add_node("welcome", welcome)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_node("human_review_node", human_review_node)

    graph_builder.add_edge(START, "welcome")
    graph_builder.add_edge("welcome", "chatbot")
    graph_builder.add_conditional_edges(
        "chatbot",
        route_after_llm,
    )
    graph_builder.add_edge("tools", "chatbot")
    # graph_builder.add_edge("chatbot", END)

    # Compile and run graph
    graph = graph_builder.compile(checkpointer=memory)
    Image.open(BytesIO(graph.get_graph().draw_mermaid_png())).show()

    def stream_graph_updates(update: dict):
        snapshot = graph.get_state(config)
        print("STATE MESSAGES:")
        for message in snapshot.values.get("messages", []):
            print(repr(message))

        events = graph.stream(
            update,
            config,
            stream_mode="updates",
            # stream_mode="values",
        )
        print("STREAM EVENTS")
        for event in events:
            print(repr(event))
            if "messages" in event:
                message = event["messages"][-1]
                message.pretty_print()

    stream_graph_updates({"messages": []})
    while True:
        # Check if we have reached a human review
        state = graph.get_state(config)
        if len(state.next):
            if state.next[0] == "human_review_node":
                human_review_input = input("Continue with tool call? ([y]/n)")
                if "n" in human_review_input:
                    print("Exiting due to human intervention.")
                    break

                stream_graph_updates(Command(resume={}))

        # Else get user input
        else:
            user_input = input("User: ")
            stream_graph_updates(
                {"messages": [{"role": "user", "content": user_input}]}
            )


@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]


@tool
def arxiv_search(topic: str) -> list[dict]:
    """Tool for searching arXiv papers."""
    papers = search_arxiv_papers(topic)
    if len(papers) == 0:
        raise ValueError(f"No papers found for topic: {topic}")
    return papers


def parse_arxiv_xml(xml_string: str) -> dict:
    # Define namespaces
    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
        "arxiv": "http://arxiv.org/schemas/atom",
    }

    root = ET.fromstring(xml_string)

    feed = {
        "title": (
            root.find("atom:title", namespaces).text
            if root.find("atom:title", namespaces) is not None
            else ""
        ),
        "id": (
            root.find("atom:id", namespaces).text
            if root.find("atom:id", namespaces) is not None
            else ""
        ),
        "updated": (
            root.find("atom:updated", namespaces).text
            if root.find("atom:updated", namespaces) is not None
            else ""
        ),
        "totalResults": (
            root.find("opensearch:totalResults", namespaces).text
            if root.find("opensearch:totalResults", namespaces) is not None
            else ""
        ),
        "startIndex": (
            root.find("opensearch:startIndex", namespaces).text
            if root.find("opensearch:startIndex", namespaces) is not None
            else ""
        ),
        "itemsPerPage": (
            root.find("opensearch:itemsPerPage", namespaces).text
            if root.find("opensearch:itemsPerPage", namespaces) is not None
            else ""
        ),
        "entries": [],
    }

    for entry in root.findall("atom:entry", namespaces):
        authors = [
            author.find("atom:name", namespaces).text
            for author in entry.findall("atom:author", namespaces)
        ]
        categories = [
            category.attrib.get("term", "")
            for category in entry.findall("atom:category", namespaces)
        ]

        entry_data = {
            "id": entry.find("atom:id", namespaces).text,
            "updated": entry.find("atom:updated", namespaces).text,
            "published": entry.find("atom:published", namespaces).text,
            "title": entry.find("atom:title", namespaces).text,
            "summary": entry.find("atom:summary", namespaces).text.strip(),
            "authors": authors,
            "comment": (
                entry.find("arxiv:comment", namespaces).text
                if entry.find("arxiv:comment", namespaces) is not None
                else ""
            ),
            "journal_ref": (
                entry.find("arxiv:journal_ref", namespaces).text
                if entry.find("arxiv:journal_ref", namespaces) is not None
                else ""
            ),
            "doi": (
                entry.find("arxiv:doi", namespaces).text
                if entry.find("arxiv:doi", namespaces) is not None
                else ""
            ),
            "links": {
                link.attrib.get("title", "default"): link.attrib.get("href", "")
                for link in entry.findall("atom:link", namespaces)
            },
            "primary_category": (
                entry.find("arxiv:primary_category", namespaces).attrib.get("term", "")
                if entry.find("arxiv:primary_category", namespaces) is not None
                else ""
            ),
            "categories": categories,
        }

        feed["entries"].append(entry_data)

    return feed


def search_arxiv_papers(topic: str, max_results: int = 10) -> dict:
    # Parse query
    query = "+".join(topic.lower().split())
    for char in list('()" '):
        if char in query:
            raise ValueError(f"Cannot have character: '{char}' in query: {query}")

    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
    resp = requests.get(url)
    if not resp.ok:
        raise ValueError(f"Bad response from arXiv API: {resp}\n{resp.text}")

    data = parse_arxiv_xml(resp.text)
    return data
