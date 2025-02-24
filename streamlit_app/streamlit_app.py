import streamlit as st
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import tempfile
import os

st.title("PDF to Markdown Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

use_llm = st.checkbox("Use LLM for better accuracy", value=False)
force_ocr = st.checkbox("Force OCR", value=False)
strip_existing_ocr = st.checkbox("Strip existing OCR", value=False)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        converter = PdfConverter(
            artifact_dict=create_model_dict(),
            use_llm=use_llm,
            force_ocr=force_ocr,
            strip_existing_ocr=strip_existing_ocr
        )
        rendered = converter(tmp_file_path)
        text, _, images = text_from_rendered(rendered)
        
        st.markdown("### Converted Text:")
        st.text_area("Markdown Output", text, height=500)
        
        if images:
            st.markdown("### Extracted Images:")
            for img in images:
                st.image(img)
    
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
    
    finally:
        os.unlink(tmp_file_path)  # Clean up temporary file
