from fastapi import FastAPI, UploadFile, File
import mimetypes

from app.parsing import extract_text_from_pdf, extract_text_from_docx
from app.embeddings import chunk_text, embed_text_chunks

app = FastAPI(title="VeriQuery API")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

    mime_type, _ = mimetypes.guess_type(file.filename)

    if mime_type == 'application/pdf':
        text = extract_text_from_pdf(content)
    elif mime_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
        text = extract_text_from_docx(content)
    else:
        return {"error": "Unsupported file type. Please upload a PDF or Word document."}

    # Chunk and embed text (for now, just chunking to show flow)
    chunks = chunk_text(text)
    embeddings = embed_text_chunks(chunks)

    return {
        "filename": file.filename,
        "text_excerpt": text[:500],
        "num_chunks": len(chunks),
    }
