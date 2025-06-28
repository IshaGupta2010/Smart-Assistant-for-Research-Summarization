from transformers import pipeline

# Load QA model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
generator = pipeline("text-generation", model="gpt2")

def generate_questions(document_text: str, num_questions: int = 3):
    questions = []
    prompt = f"Generate {num_questions} comprehension questions from this document:\n{document_text[:1000]}"

    output = generator(prompt, max_length=150, num_return_sequences=1, do_sample=True)[0]["generated_text"]
    
    # Simple line-split fallback
    for line in output.split("\n"):
        if "?" in line and len(questions) < num_questions:
            questions.append(line.strip())

    # Backup: force 3 basic prompts if not enough generated
    while len(questions) < num_questions:
        questions.append("What is one key point mentioned in the document?")
    
    return questions

def evaluate_user_answer(document_text: str, question: str, user_answer: str):
    qa_result = qa_pipeline(question=question, context=document_text)
    correct_answer = qa_result["answer"]
    confidence = qa_result["score"]

    # Basic comparison
    is_correct = user_answer.strip().lower() in correct_answer.lower()

    justification = ""
    start = document_text.find(correct_answer)
    if start != -1:
        snippet_start = max(0, start - 100)
        snippet_end = min(len(document_text), start + 100)
        justification = document_text[snippet_start:snippet_end]

    return {
        "is_correct": is_correct,
        "correct_answer": correct_answer,
        "confidence": confidence,
        "justification": justification.strip()
    }
