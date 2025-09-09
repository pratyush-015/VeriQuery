from fastapi import FastAPI, UploadFile, File
import mimetypes
from app.parsing import extract_text_from_pdf, extract_text_from_docx
from app.embeddings import chunk_text, embed_text_chunks, rerank_chunks
from app.llm import answer_with_llm
from app.query_parsing import extract_entities
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from sentence_transformers import SentenceTransformer

app = FastAPI(title="VeriQuery API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

doc_chunks = []
chunk_embeddings = []

model = SentenceTransformer('all-MiniLM-L6-v2')

class QueryRequest(BaseModel):
    question: str

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

    # Use semantic chunking for better splits
    chunks = chunk_text(text)
    embeddings = embed_text_chunks(chunks)

    global doc_chunks, chunk_embeddings
    doc_chunks += chunks
    chunk_embeddings += [e.tolist() for e in embeddings]

    return {
        "filename": file.filename,
        "text_excerpt": text[:500],
        "num_chunks": len(chunks),
    }


@app.post("/query")
async def query_document(req: QueryRequest):
    question = req.question
    query_embedding = model.encode([question])[0]

    # Rerank chunks based on semantic similarity
    top_chunks, top_idxs = rerank_chunks(query_embedding, chunk_embeddings, doc_chunks, top_k=3)
    context = "\n".join(top_chunks)

    entities = extract_entities(question)

    # Call LLM to get answer
    result = answer_with_llm(question, context)

    decision = result.get("decision", "unknown")
    amount = result.get("amount", None)
    answer = result.get("answer", "")
    clause_mapping = result.get("clause_mapping", {})

    justification = []
    for comp, idx in clause_mapping.items():
        idx_int = idx if isinstance(idx, int) else int(idx)
        justification.append({
            "decision_component": comp,
            "clause": idx_int,
            "text": top_chunks[idx_int] if idx_int < len(top_chunks) else ""
        })

    return {
        "question": question,
        "decision": decision,
        "amount": amount,
        "answer": answer,
        "justification": justification,
        "source_clauses": top_chunks,
    }
