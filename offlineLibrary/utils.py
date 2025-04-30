import fitz  # PyMuPDF
import os

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return text

def generate_pdf_thumbnail(pdf_path, thumbnail_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # first page
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # scale up if needed

    os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

    pix.save(thumbnail_path)
    return thumbnail_path
