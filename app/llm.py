from transformers import pipeline

# Load only once at module level (avoid reloading on every request)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def answer_with_llm(question: str, context: str) -> dict:
    try:
        result = qa_pipeline(question=question, context=context)
        return {
            "answer": result.get("answer"),
            "score": float(result.get("score"))
        }
    except Exception as e:
        return {"error": str(e)}
