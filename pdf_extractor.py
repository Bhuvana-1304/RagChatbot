import fitz

def extract_text_from_pdf(file_path):
    """
    Extracts all text from the given PDF file.
    """
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text("text")
    return text
