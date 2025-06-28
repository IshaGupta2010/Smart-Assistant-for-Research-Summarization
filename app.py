import streamlit as st
from utils.parser import extract_text_from_file
from utils.summarizer import generate_summary
from utils.qa import answer_question  # ✅ Existing import
from utils.challenge import generate_questions, evaluate_user_answer  # ✅ Newly added
from utils.memory import load_memory, save_memory, clear_memory

chat_history = load_memory()

st.set_page_config(page_title="Smart Assistant", layout="wide")
st.title("📚 Smart Assistant for Research Summarization")

st.sidebar.title("Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])

document_text = ""

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    # Extract text
    document_text = extract_text_from_file(uploaded_file)

    if document_text:
        # Auto Summary (≤ 150 words)
        with st.spinner("Generating summary..."):
            summary = generate_summary(document_text)
            st.subheader("📝 Auto Summary (≤ 150 words)")
            st.write(summary)

        # Show partial content for inspection
        st.subheader("📄 Extracted Document Content")
        st.text_area("Text Extracted:", document_text[:3000], height=300)

        # ✅ Ask Anything mode with memory
        st.subheader("🧠 Ask Anything (based on document)")
        user_question = st.text_input("Enter your question:")

        if user_question:
            with st.spinner("Thinking..."):
                result = answer_question(document_text, user_question)
                answer = result["answer"]
                justification = result["justification"].replace(answer, f"<mark>{answer}</mark>")

                chat_history.append({
                    "question": user_question,
                    "answer": answer,
                    "justification": justification
                })
                save_memory(chat_history)

                st.markdown(f"**Answer:** {answer}")
                st.markdown(f"**Confidence:** {result['confidence']:.2f}")
                st.markdown("**Justification Snippet:**", unsafe_allow_html=True)
                st.markdown(
                    f"<div style='background-color:#f9f9f9; padding:10px; border-radius:5px'>{justification}</div>",
                    unsafe_allow_html=True
                )

                # 🔍 Full context highlighting in the extracted document
                start = result.get("start_idx", document_text.find(answer))
                if start != -1:
                    highlighted_text = (
                        document_text[:start] +
                        f"<mark>{answer}</mark>" +
                        document_text[start + len(answer):]
                    )
                    st.subheader("📌 Full Document Highlighted View")
                    st.markdown(
                        f"<div style='background-color:#f0f0f0; padding:10px; max-height:300px; overflow:auto; border-radius:6px'>{highlighted_text}</div>",
                        unsafe_allow_html=True
                    )


        if chat_history:
            st.subheader("🗃️ Chat Memory (Persistent)")
            for i, qa in enumerate(chat_history, 1):
                st.markdown(f"**Q{i}:** {qa['question']}")
                st.markdown(f"**A{i}:** {qa['answer']}")
                st.markdown(f"Justification: {qa['justification']}", unsafe_allow_html=True)

        if st.button("🧹 Clear Memory"):
            clear_memory()
            st.success("Memory cleared!")

        # ✅ Challenge Me mode
        st.subheader("🧩 Challenge Me (Test Your Understanding)")
        if st.button("Generate Challenge Questions"):
            st.session_state.questions = generate_questions(document_text)

        if "questions" in st.session_state:
            for i, q in enumerate(st.session_state.questions):
                st.markdown(f"**Q{i+1}. {q}**")
                user_input = st.text_input(f"Your Answer {i+1}", key=f"ans_{i}")

                if user_input:
                    result = evaluate_user_answer(document_text, q, user_input)
                    st.success("✅ Correct!" if result["is_correct"] else "❌ Incorrect.")
                    st.markdown(f"**Expected Answer:** {result['correct_answer']}")
                    st.markdown(f"**Justification:** {result['justification']}")

    else:
        st.warning("No readable text found in the uploaded file.")
else:
    st.info("📂 Please upload a document to begin.")
