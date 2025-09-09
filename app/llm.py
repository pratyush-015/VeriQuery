from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def build_prompt(question, contexts):
    joined_context = "\n\n".join([f"Section:\n{ctx}" for ctx in contexts])
    return (
        f"Answer the question ONLY using the following document excerpts.\n"
        f"If the information is not available, explicitly say 'unknown'.\n"
        f"Provide your answer strictly in this JSON format:\n"
        f"{{\"decision\": string, \"answer\": string, \"clause_mapping\": object}}\n\n"
        f"Question: {question}\n"
        f"Context:\n{joined_context}\n"
    )


def answer_with_llm(question: str, context: str) -> dict:
    try:
        if not context or not context.strip():
            return {
                "decision": "unknown",
                "answer": "No content available to answer the question.",
                "score": 0.0,
                "clause_mapping": {}
            }

        result = qa_pipeline(question=question, context=context)
        answer = result.get("answer", "")
        score = float(result.get("score", 0.0))

        if not answer or answer.strip().lower() in ["", "unknown", "no answer"]:
            decision = "unknown"
        elif score > 0.2:
            decision = "answered"
        else:
            decision = "unknown"

        # Example: mock clause mapping logic (can be improved)
        clause_mapping = {"relevant_clause": 0}

        return {
            "decision": decision,
            "answer": answer,
            "score": score,
            "clause_mapping": clause_mapping
        }
    except Exception as e:
        return {
            "decision": "error",
            "answer": "",
            "score": 0.0,
            "clause_mapping": {},
            "error": str(e)
        }
