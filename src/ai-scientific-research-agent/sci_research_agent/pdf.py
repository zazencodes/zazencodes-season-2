import io
import logging

import PyPDF2
import requests
from langchain_core.tools import tool

# Setup module logger
logger = logging.getLogger(__name__)


@tool
def read_pdf(url: str) -> str:
    """Read and extract text from a PDF file given its URL.

    Args:
        url: The URL of the PDF file to read

    Returns:
        The extracted text content from the PDF
    """
    try:
        logger.info(f"Downloading PDF from URL: {url}")
        # Download PDF
        response = requests.get(url)
        response.raise_for_status()
        logger.info("Successfully downloaded PDF")

        # Create PDF reader object
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        logger.info(f"PDF has {num_pages} pages")

        # Extract text from all pages
        text = ""
        for i, page in enumerate(pdf_reader.pages, 1):
            logger.info(f"Extracting text from page {i}/{num_pages}")
            text += page.extract_text() + "\n"

        logger.info(f"Successfully extracted {len(text)} characters of text from PDF")
        return text.strip()
    except Exception as e:
        logger.error(f"Error reading PDF: {str(e)}")
        raise
