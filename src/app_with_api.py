import streamlit as st
import json
from components.file_upload import upload_file
from services.pdf_processor import process_pdf
from components.json_display import display_json
import threading
import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Page configuration
st.set_page_config(
    page_title="PDF Processor",
    page_icon="📄",
    layout="wide"
)

# FastAPI app
api_app = FastAPI(
    title="PDF Processor API",
    description="API for extracting text, metadata, and images from PDF files",
    version="1.0.0"
)

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "PDF Processor API"}

@api_app.post("/api/process-pdf")
async def process_pdf_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Handle the uploaded file directly
        pdf_bytes = await file.read()
        
        # Create a temporary file-like object
        class TempFile:
            def __init__(self, content):
                self.content = content
                self.position = 0
            
            def read(self):
                return self.content
        
        temp_file = TempFile(pdf_bytes)
        result = process_pdf(temp_file)
        parsed_result = json.loads(result)
        
        return JSONResponse(content=parsed_result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

def run_api_server():
    """Run the FastAPI server in a separate thread"""
    uvicorn.run(api_app, host="0.0.0.0", port=8000, log_level="error")

# Start API server in background
if 'api_started' not in st.session_state:
    st.session_state.api_started = True
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    api_thread.start()
    time.sleep(2)  # Give the server time to start

def main():
    st.title("📄 PDF Data Extractor")
    
    # Create tabs for UI and API info
    tab1, tab2 = st.tabs(["🖥️ Web Interface", "🔌 API Access"])
    
    with tab1:
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
    
    with tab2:
        st.markdown("## 🔌 API Endpoints")
        st.markdown("The following API endpoints are available for programmatic access:")
        
        # Get the current URL
        if 'streamlit' in st.__file__:
            # Running on Streamlit Cloud
            base_url = "https://app-pdf-proceappr-cnebznxghmgzab8rpvgxvq.streamlit.app"
        else:
            # Running locally
            base_url = "http://localhost:8501"
        
        api_base_url = base_url.replace(":8501", ":8000")
        
        st.code(f"""
# Health Check
GET {api_base_url}/api/health

# Process PDF
POST {api_base_url}/api/process-pdf
Content-Type: multipart/form-data
Body: PDF file as form data with key 'file'
        """)
        
        st.markdown("### 🐍 Python Example")
        st.code(f"""
import requests

# Health check
response = requests.get("{api_base_url}/api/health")
print(response.json())

# Process PDF
with open("document.pdf", "rb") as f:
    files = {{"file": ("document.pdf", f, "application/pdf")}}
    response = requests.post("{api_base_url}/api/process-pdf", files=files)
    result = response.json()
    print(f"Pages: {{result['metadata']['pageCount']}}")
        """)
        
        st.markdown("### 📱 cURL Example")
        st.code(f"""
# Health check
curl {api_base_url}/api/health

# Process PDF
curl -X POST \\
  -F "file=@document.pdf" \\
  {api_base_url}/api/process-pdf
        """)
        
        st.markdown("### ⚠️ Note")
        st.info("""
        This embedded API works when running locally. For production use, consider deploying 
        the FastAPI separately to platforms like Railway, Render, or Heroku for better performance 
        and reliability.
        """)

if __name__ == "__main__":
    main()
