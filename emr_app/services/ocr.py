import os

def extract_text_from_file(path, mime=""):
    """Very small stub:
    - If a .txt file, read directly.
    - If a PDF/image or other, return a placeholder string.
    Replace later with real OCR/PDF parsing.
    """
    try:
        if path.lower().endswith(".txt"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        # TODO: integrate PyPDF2 / pdfminer / pytesseract
        return f"[text extraction pending for {os.path.basename(path)}; mime={mime}]"
    except Exception as e:
        return f"[extraction error: {e}]"
