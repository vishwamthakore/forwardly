import re
from datetime import datetime


def clean_string(text: str) -> str:
    if not text:
        return "unknown"

    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)   # remove special chars
    text = re.sub(r"\s+", "-", text)       # replace spaces with dash
    text = re.sub(r"-+", "-", text)        # remove duplicate dashes
    return text.strip("-")


def generate_jd_name(parsed_json: dict) -> str:
    company = clean_string(parsed_json.get("company_name"))
    role = clean_string(parsed_json.get("job_title"))

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    return f"{company}-{role}-{timestamp}"