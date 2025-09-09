import fitz  # PyMuPDF
import docx
import re

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


def semantic_chunk(text: str, min_len=150, max_len=500) -> list[str]:
    """
    Splits a long text into semantically meaningful chunks by paragraphs or clause headings.
    """
    # Split by double line breaks or common clause headings
    splits = re.split(r'\n\s*\n|Clause \d+\.?\d*|Section \d+\.?\d*', text)
    chunks = []
    buffer = ""

    for seg in splits:
        seg = seg.strip()
        if not seg:
            continue
        if len(buffer) + len(seg) < min_len:
            buffer += " " + seg
        else:
            if buffer:
                chunks.append(buffer.strip())
            buffer = seg
    if buffer:
        chunks.append(buffer.strip())

    # Further split chunks exceeding max_len
    final_chunks = []
    for chunk in chunks:
        while len(chunk) > max_len:
            final_chunks.append(chunk[:max_len])
            chunk = chunk[max_len:]
        if chunk:
            final_chunks.append(chunk)

    return final_chunks
