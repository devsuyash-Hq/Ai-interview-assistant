"""
Resume Parser
=============
Extracts raw text from a candidate's resume (PDF) so it can be
passed to the AI engine for structured summarization.
"""

import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all readable text from a PDF resume.

    Args:
        pdf_path: Path to the resume PDF file.

    Returns:
        Full extracted text, pages joined by newlines.

    Raises:
        FileNotFoundError: if the path does not exist.
    """
    text_chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
    return "\n".join(text_chunks)
