import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open("pdf", file_bytes) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    with open("temp.docx", "wb") as f:
        f.write(file_bytes)
    document = docx.Document("temp.docx")
    text = "\n".join([para.text for para in document.paragraphs])
    return text

def check_missing_entities(entities: dict, required_fields: list) -> list:
    """
    Returns list of fields missing from extracted entities.
    """
    missing = [field for field in required_fields if field not in entities or not entities[field]]
    return missing

