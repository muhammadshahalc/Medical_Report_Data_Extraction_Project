#preprocessing.py
import re

def preprocess_text(text: str) -> str:
    """
    Clean up text by removing extra spaces and line breaks.
    """
    if not text:
        return ""
    text = re.sub(r"\n+", " ", text)            # Replace multiple newlines with space
    text = re.sub(r"\s{2,}", " ", text)         # Replace multiple spaces with single space
    return text.strip()
