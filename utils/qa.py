from transformers import pipeline

# Load QA model from Hugging Face
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def answer_question(context: str, question: str):
    result = qa_pipeline(question=question, context=context)
    
    # Extract the answer and confidence
    answer = result['answer']
    confidence = result['score']
    
    # Justification (we'll use a rough sentence match here for now)
    start = context.find(answer)
    justification = ""
    if start != -1:
        # Get a snippet around the answer for context
        snippet_start = max(0, start - 100)
        snippet_end = min(len(context), start + 100)
        justification = context[snippet_start:snippet_end]

    return {
        "answer": answer,
        "confidence": confidence,
        "justification": justification.strip(),
        "start_idx": start
    }
