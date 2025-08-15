from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import uvicorn
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.pdf_processor import process_pdf
import tempfile

app = FastAPI(
    title="PDF Processor API",
    description="API for extracting text, metadata, and images from PDF files",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "PDF Processor API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "process_pdf": "/process-pdf",
            "process_pdf_metadata_only": "/process-pdf-metadata-only"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "PDF Processor API"}

@app.post("/process-pdf")
async def process_pdf_endpoint(file: UploadFile = File(...)):
    """
    Process a PDF file and extract text, metadata, and images.
    
    Returns:
    - text: Extracted text content
    - metadata: Document metadata (title, author, page count, etc.)
    - images: Base64 encoded images found in the PDF
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Process the PDF using your existing function
        result = process_pdf(temp_file_path)
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        # Parse the JSON result
        parsed_result = json.loads(result)
        
        # Return the result
        return JSONResponse(content=parsed_result)
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/process-pdf-metadata-only")
async def process_pdf_metadata_only(file: UploadFile = File(...)):
    """
    Process a PDF file and extract only metadata (faster processing).
    
    Returns:
    - metadata: Document metadata (title, author, page count, etc.)
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        import fitz
        
        # Read the PDF content
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")
        
        # Extract only metadata
        metadata = doc.metadata
        result = {
            "metadata": {
                "pageCount": len(doc),
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "creationDate": metadata.get("creationDate", ""),
                "modificationDate": metadata.get("modDate", "")
            }
        }
        
        doc.close()
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF metadata: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
