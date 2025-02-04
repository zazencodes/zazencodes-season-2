import logging
import subprocess
import tempfile
from pathlib import Path

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF.

    Args:
        latex_content: The LaTeX document content as a string

    Returns:
        Path to the generated PDF file
    """
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Write LaTeX content to file
            tex_file = temp_path / "paper.tex"
            tex_file.write_text(latex_content)
            logger.info(f"Wrote LaTeX content to {tex_file}")

            # Run latexmk to compile the PDF
            logger.info("Compiling LaTeX to PDF...")
            result = subprocess.run(
                ["latexmk", "-pdf", "-interaction=nonstopmode", str(tex_file)],
                cwd=temp_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                logger.error(f"LaTeX compilation failed: {result.stderr}")
                raise RuntimeError(f"LaTeX compilation failed: {result.stderr}")

            # Copy PDF to a more permanent location
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)

            pdf_file = temp_path / "paper.pdf"
            final_pdf = output_dir / "paper.pdf"

            if not pdf_file.exists():
                raise FileNotFoundError("PDF file was not generated")

            # Copy the PDF file
            final_pdf.write_bytes(pdf_file.read_bytes())
            logger.info(f"Successfully generated PDF at {final_pdf}")

            return str(final_pdf)

    except Exception as e:
        logger.error(f"Error rendering LaTeX: {str(e)}")
        raise


# Example LaTeX content to test
latex_content = r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{hyperref}

\title{Sample LaTeX Document}
\author{John Doe}
\date{\today}

\begin{document}

\maketitle

This is a sample document with an author and title.

Here is an inline math formula: $E = mc^2$.

And here is a display equation:
\[
\frac{d}{dx}e^x = e^x
\]

\section{Introduction}

This is the introduction section of the document. You can add more sections, figures, and references as needed.

\end{document}
"""

# Call the function to render PDF
pdf_path = render_latex_pdf(latex_content)
print(f"PDF generated at: {pdf_path}")
