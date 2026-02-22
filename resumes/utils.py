import os
import re
import shutil
import unicodedata
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile
from config.exceptions import InvalidFileUploadException

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def upload_pdf_file(file: UploadFile):
    # 1) check filename exists
    if not file.filename:
        raise InvalidFileUploadException(message="No file provided")

    # 2) allow only pdf extension
    if not file.filename.lower().endswith(".pdf"):
        raise InvalidFileUploadException(message="Only PDF files are allowed")

    # 3) check content-type (important)
    if file.content_type != "application/pdf":
        raise InvalidFileUploadException(message="Invalid file type")

    original_filename = file.filename
    clean_filename = get_clean_resume_filename(original_filename)
    save_path = UPLOAD_DIR / clean_filename

    # 4) save file (streaming copy, memory safe)
    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return clean_filename


def get_clean_resume_filename(original_filename: str) -> str:
    """
    Clean and normalize uploaded resume filename and make it unique.

    Example:
    "Vishwam  Thakore Resume!!.pdf"
    ->
    "vishwam-thakore-resume-2026-02-22_19-04-33.pdf"
    """

    # -------- 1. Remove path (security) --------
    # prevents ../../etc/passwd attacks
    filename = os.path.basename(original_filename)

    # -------- 2. Split extension --------
    name, ext = os.path.splitext(filename)

    # Normalize extension
    ext = ext.lower()

    # -------- 3. Unicode normalization --------
    # résumé -> resume
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")

    # -------- 4. Remove unwanted characters --------
    # keep letters, numbers, spaces, dash, underscore
    name = re.sub(r"[^a-zA-Z0-9\s_-]", "", name)

    # -------- 5. Remove extra spaces --------
    name = re.sub(r"\s+", " ", name).strip()

    # -------- 6. Replace spaces with dash --------
    name = name.replace(" ", "-")

    # Lowercase for consistency
    name = name.lower()

    # Edge case: empty filename
    if not name:
        name = "resume"

    # -------- 7. Add human readable timestamp --------
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # -------- 8. Final filename --------
    final_filename = f"{name}-{timestamp}{ext}"

    return final_filename