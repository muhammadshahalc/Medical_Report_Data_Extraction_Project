import pdfplumber
import pytesseract
from typing import List, Dict

def extract_text_from_pdfs(pdf_paths: List[str]) -> Dict[str, str]:
    """
    Extract text from multiple PDFs using pdfplumber and OCR for image PDFs.
    """
    results = {}
    
    for pdf_path in pdf_paths:
        text = ""
        try:
            # Try digital PDF extraction
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            # If nothing extracted, apply OCR
            if not text.strip():
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        pil_img = page.to_image(resolution=300).original
                        text += pytesseract.image_to_string(pil_img) + "\n"
            
            results[pdf_path] = text.strip()
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            results[pdf_path] = ""
    
    return results
