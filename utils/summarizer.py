from transformers import pipeline

# ✅ Removed all NLTK-related code

# Load summarizer pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def chunk_text(text, max_chunk=500):
    """Split text into chunks for long document summarization using simple split."""
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) <= max_chunk:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def generate_summary(text: str, word_limit: int = 150) -> str:
    chunks = chunk_text(text)

    summarized_chunks = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summarized_chunks.append(summary[0]['summary_text'])

    full_summary = " ".join(summarized_chunks)
    return full_summary[:word_limit * 6]  # roughly limit by word count
