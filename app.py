import streamlit as st
import tempfile
from ocr import extract_text_from_pdf
from parser import extract_invoice_data
from validator import calculate_confidence

st.title("Invoice Parser")

uploaded_file = st.file_uploader("Upload Invoice PDF", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    st.success("File uploaded successfully!")

    # Run pipeline
    text = extract_text_from_pdf(temp_path)
    data = extract_invoice_data(text)
    confidence = calculate_confidence(data)

    # Display results
    st.subheader("Extracted Data")

    for key, value in data.items():
        st.write(f"**{key.capitalize()}**: {value}")

    st.subheader("Raw JSON Output")
    st.json(data)

    st.subheader("Confidence Score")
    st.write(f"{confidence}%")