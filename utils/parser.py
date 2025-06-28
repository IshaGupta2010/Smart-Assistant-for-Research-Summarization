import io
from pdfminer.high_level import extract_text
import streamlit as st

def extract_text_from_pdf(uploaded_pdf) -> str:
    # Read PDF content from the uploaded file
    text = extract_text(uploaded_pdf)
    return text.strip()

def extract_text_from_txt(uploaded_txt) -> str:
    # Decode the bytes into string
    return uploaded_txt.read().decode('utf-8').strip()

def extract_text_from_file(uploaded_file) -> str:
    file_type = uploaded_file.type
    if file_type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type == "text/plain":
        return extract_text_from_txt(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF or TXT file.")
        return ""
