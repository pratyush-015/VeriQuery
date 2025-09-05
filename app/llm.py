from transformers import pipeline

# Load only once at module level (avoid reloading on every request)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def answer_with_llm(question: str, context: str) -> dict:
    try:
        if not context or not context.strip():
            # No document content to provide answer from
            return {
                "decision": "unknown",
                "answer": "No content available to answer the question.",
                "score": 0.0,
                "clause_mapping": {}
            }
        
        result = qa_pipeline(question=question, context=context)
        answer = result.get("answer", "")
        score = float(result.get("score", 0.0))

        # Apply simple logic: If the model's answer is empty/irrelevant, decision is 'unknown'
        if not answer or answer.strip().lower() in ["", "unknown", "no answer"]:
            decision = "unknown"
        elif score > 0.2:  # Threshold for trusting answer, tune as needed
            decision = "answered"
        else:
            decision = "unknown"

        return {
            "decision": decision,
            "answer": answer,
            "score": score,
            "clause_mapping": {}
        }
    except Exception as e:
        return {
            "decision": "error",
            "answer": "",
            "score": 0.0,
            "clause_mapping": {},
            "error": str(e)
        }
