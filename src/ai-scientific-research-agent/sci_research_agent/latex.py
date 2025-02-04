import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path

from langchain_core.tools import tool

# Setup module logger
logger = logging.getLogger(__name__)


@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF.

    Args:
        latex_content: The LaTeX document content as a string

    Returns:
        Path to the generated PDF file
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = Path("output").absolute()
        output_dir.mkdir(exist_ok=True)

        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tex_filename = f"paper_{timestamp}.tex"
        pdf_filename = f"paper_{timestamp}.pdf"

        # Write LaTeX content to file
        tex_file = output_dir / tex_filename
        tex_file.write_text(latex_content)
        logger.info(f"Wrote LaTeX content to {tex_file}")

        # Run latexmk to compile the PDF
        logger.info("Compiling LaTeX to PDF...")
        result = subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", str(tex_file)],
            cwd=output_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            logger.error(f"LaTeX compilation failed: {result.stderr}")
            raise RuntimeError(f"LaTeX compilation failed: {result.stderr}")

        final_pdf = output_dir / pdf_filename

        if not final_pdf.exists():
            raise FileNotFoundError("PDF file was not generated")

        logger.info(f"Successfully generated PDF at {final_pdf}")
        return str(final_pdf)

    except Exception as e:
        logger.error(f"Error rendering LaTeX: {str(e)}")
        raise
