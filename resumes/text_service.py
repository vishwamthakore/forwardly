import pdfplumber
import re
from resumes.utils import UPLOAD_DIR


def extract_text_from_pdf(path: str) -> str:
    """
    Layout-aware extraction.
    Uses tolerances tuned for resumes.
    """
    pages_text = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:

            text = page.extract_text(
                x_tolerance=1,  # controls horizontal word joining
                y_tolerance=3,  # controls line grouping
                layout=True,  # VERY important for multi-column resumes
            )

            if text:
                pages_text.append(text)

    return "\n".join(pages_text)


def clean_resume_text(text: str) -> str:
    """
    Prepare resume text for LLM parsing.
    """

    # 1. Normalize line endings
    text = text.replace("\r", "\n")

    # 2. Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # 3. Remove repeated blank lines
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    # 4. Fix broken words (common in PDFs)
    # Example: "Develop-\nment" -> "Development"
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # 5. Join wrapped lines inside paragraphs
    # resumes often break lines at 80 char width
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # 6. Restore section spacing
    # ensure headings separated
    text = re.sub(
        r"(Education|Experience|Skills|Projects|Summary)", r"\n\n\1", text, flags=re.I
    )

    # 7. Remove page numbers
    text = re.sub(r"\n?\s*Page \d+\s*\n?", "\n", text, flags=re.I)

    # 8. Strip leading/trailing whitespace
    text = text.strip()

    return text


def get_clean_text_from_pdf(filename: str) -> str:

    path = UPLOAD_DIR / filename
    raw_text = extract_text_from_pdf(path)

    if not raw_text or len(raw_text.strip()) < 50:
        raise ValueError("Could not extract meaningful text from PDF")

    cleaned_text = clean_resume_text(raw_text)

    return cleaned_text
