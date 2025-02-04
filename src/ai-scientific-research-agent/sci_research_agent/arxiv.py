import xml.etree.ElementTree as ET
import logging

import requests
from langchain_core.tools import tool

# Setup module logger
logger = logging.getLogger(__name__)


@tool
def arxiv_search(topic: str) -> list[dict]:
    """Search for recently uploaded arXiv papers

    Args:
        topic: The topic to search for papers about

    Returns:
        List of papers with their metadata including title, authors, summary, etc.
    """
    logger.info(f"Searching arXiv for papers about: {topic}")
    papers = search_arxiv_papers(topic)
    if len(papers) == 0:
        logger.error(f"No papers found for topic: {topic}")
        raise ValueError(f"No papers found for topic: {topic}")
    logger.info(f"Found {len(papers['entries'])} papers about {topic}")
    return papers


def search_arxiv_papers(topic: str, max_results: int = 10) -> dict:
    # Parse query
    query = "+".join(topic.lower().split())
    for char in list('()" '):
        if char in query:
            logger.error(f"Invalid character '{char}' in query: {query}")
            raise ValueError(f"Cannot have character: '{char}' in query: {query}")

    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query=all:{query}"
        f"&max_results={max_results}"
        "&sortBy=submittedDate"
        "&sortOrder=descending"
    )
    logger.info(f"Making request to arXiv API: {url}")
    resp = requests.get(url)
    if not resp.ok:
        logger.error(f"ArXiv API request failed: {resp.status_code} - {resp.text}")
        raise ValueError(f"Bad response from arXiv API: {resp}\n{resp.text}")

    logger.info("Successfully retrieved response from arXiv API")
    data = parse_arxiv_xml(resp.text)
    return data


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
