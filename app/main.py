from fastapi import FastAPI, UploadFile, File, Query
import mimetypes
from app.parsing import extract_text_from_pdf, extract_text_from_docx
from app.embeddings import chunk_text, embed_text_chunks, find_relevant_chunks
from app.llm import answer_with_llm
from app.query_parsing import extract_entities
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# In-memory doc store (replace with database or persistent store for real use)
doc_chunks = []
chunk_embeddings = []

app = FastAPI(title="VeriQuery API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Chunk and embed text (for now, just chunking to show flow)
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
    # Step 1: Embed the question using the same model as chunks
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([question])[0]

    entities = extract_entities(question)

    
    # Step 2: Retrieve top-3 relevant chunks
    import numpy as np
    embs = np.array(chunk_embeddings)
    sims = np.dot(embs, query_embedding) / (np.linalg.norm(embs, axis=1) * np.linalg.norm(query_embedding))
    top_indices = sims.argsort()[-3:][::-1]
    top_chunks = [doc_chunks[i] for i in top_indices]
    context = "\n".join(top_chunks)
    
    # Step 3: Call LLM for answer
    result = answer_with_llm(question, context)
    decision = result.get("decision", "unknown")
    amount = result.get("amount", None)
    answer = result.get("answer", "")
    clause_mapping = result.get("clause_mapping", {})  # dict: component -> idx

    # Build explainable justification
    justification = []
    for comp, idx in clause_mapping.items():
        justification.append({
            "decision_component": comp,
            "clause": idx,
            "text": top_chunks[idx] if idx < len(top_chunks) else ""
        })
    
    # Step 4: Return as structured JSON
    return {
        "question": question,
        "decision": decision,
        "amount": amount,
        "answer": answer,
        "justification": justification,
        "source_clauses": top_chunks  # All retrieved chunks, for reference
    }
