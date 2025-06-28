# 📚 Smart Assistant for Research Summarization

A GenAI-powered assistant that helps users understand long documents (PDF/TXT) by:
- Summarizing the content (≤150 words)
- Answering free-form questions based on document context
- Challenging users with logic-based questions and evaluating their answers
- Providing contextual justifications and highlights
- Tracking session-based memory for follow-up queries

---

## 🛠 Features

✅ Document upload (PDF/TXT)  
✅ Auto-summary using NLP  
✅ “Ask Anything” with contextual QA  
✅ “Challenge Me” with logic-based questions  
✅ Answer evaluation with justification  
✅ Contextual answer highlighting in document  
✅ Session memory for Q&A history  
✅ Clean, interactive Streamlit UI

---

## 🧠 Architecture Overview

```plaintext
User Uploads PDF/TXT
        │
        ▼
[Extract Text] ← PDFMiner / File Reader
        │
        ├──► [Summarizer] ← DistilBART (transformers)
        │
        ├──► [Ask Anything] ← DistilBERT QA
        │       ├── Highlighted Answer in Context
        │       └── Session Memory for Q&A
        │
        └──► [Challenge Me]
               ├── Question Generator ← GPT-2
               └── Answer Evaluator  ← Fuzzy/Exact Match
```

---

## 🗂 Project Structure

```
smart-assistant-summarizer/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Dependency list
├── README.md                 # Project info & setup
└── utils/
    ├── parser.py             # Text extraction (PDF/TXT)
    ├── summarizer.py         # Summarization logic
    ├── qa.py                 # Ask Anything logic with justification
    └── challenge.py          # Challenge Me logic
```

---

## ⚙️ Setup Instructions

> 💡 Recommended: Python 3.8+ and a virtual environment

### 1. Clone the repo

```bash
git clone https://github.com/IshaGupta2010/smart-assistant-summarizer.git
cd smart-assistant-summarizer
```

### 2. Set up environment

```bash
python -m venv venv
venv\Scriptsctivate      # (Windows)
# OR
source venv/bin/activate   # (Mac/Linux)
```


### 4. Run the app locally

```bash
streamlit run app.py
```

---

## 📦 Dependencies

All required in `requirements.txt`:

- `streamlit`
- `transformers`
- `torch`
- `pdfminer.six`
- `nltk`
- `pandas`

---

## 💡 Future Enhancements

- User-authenticated persistent memory  
- Multi-document Q&A comparison  
- Fine-tuned LLMs for specific academic domains

---

## 👩‍💻 Built by
**Isha Gupta** | AI/ML & Full-Stack Developer | [LinkedIn](https://linkedin.com/in/isha-gupta) | [GitHub](https://github.com/IshaGupta2010)