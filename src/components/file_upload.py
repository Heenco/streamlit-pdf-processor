import streamlit as st

def upload_file():
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a PDF file to extract text, metadata, and images. Maximum file size: 200MB"
    )
    
    if uploaded_file is not None:
        # Validate file size (200MB limit)
        max_size = 200 * 1024 * 1024  # 200MB in bytes
        if uploaded_file.size > max_size:
            st.error(f"❌ File too large! Maximum size is 200MB. Your file is {uploaded_file.size / (1024*1024):.1f}MB")
            return None
        
        return uploaded_file
    return None