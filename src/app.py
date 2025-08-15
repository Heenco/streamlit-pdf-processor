import streamlit as st
import json
from components.file_upload import upload_file
from services.pdf_processor import process_pdf
from components.json_display import display_json

# Page configuration
st.set_page_config(
    page_title="PDF Processor",
    page_icon="📄",
    layout="wide"
)

def main():
    st.title("📄 PDF Data Extractor")
    st.markdown("""
    Upload a PDF file to extract:
    - 📝 **Text content** from all pages
    - 📊 **Document metadata** (title, author, page count, etc.)
    - 🖼️ **Images** embedded in the document
    """)

    # File upload
    pdf_file = upload_file()

    if pdf_file is not None:
        # Show file details
        st.success(f"✅ File uploaded: {pdf_file.name} ({pdf_file.size:,} bytes)")
        
        # Process the PDF file with progress indicator
        with st.spinner("🔄 Processing PDF... This may take a moment for large files."):
            result = process_pdf(pdf_file)

        # Display the result
        if result:
            display_json(result)
        else:
            st.error("❌ Error processing the PDF file.")
    else:
        st.info("👆 Please upload a PDF file to get started.")

if __name__ == "__main__":
    main()