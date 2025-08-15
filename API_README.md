# PDF Processor API

A FastAPI-based REST API for extracting text, metadata, and images from PDF files.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the API Server
```bash
python api_server.py
```

The API will be available at: `http://localhost:8000`

### 3. View API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```
GET /health
```
Returns the health status of the API.

**Response:**
```json
{
  "status": "healthy",
  "service": "PDF Processor API"
}
```

### Process PDF (Full)
```
POST /process-pdf
```
Extracts text, metadata, and images from a PDF file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: PDF file as form data with key `file`

**Response:**
```json
{
  "text": "Extracted text content...",
  "metadata": {
    "pageCount": 5,
    "title": "Document Title",
    "author": "Author Name",
    "subject": "Subject",
    "creator": "Creator",
    "producer": "Producer",
    "creationDate": "2023-01-01",
    "modificationDate": "2023-01-02"
  },
  "images": [
    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
  ]
}
```

### Process PDF (Metadata Only)
```
POST /process-pdf-metadata-only
```
Extracts only metadata from a PDF file (faster processing).

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: PDF file as form data with key `file`

**Response:**
```json
{
  "metadata": {
    "pageCount": 5,
    "title": "Document Title",
    "author": "Author Name",
    "subject": "Subject",
    "creator": "Creator",
    "producer": "Producer",
    "creationDate": "2023-01-01",
    "modificationDate": "2023-01-02"
  }
}
```

## Usage Examples

### Python (using requests)
```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Process PDF
with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    response = requests.post("http://localhost:8000/process-pdf", files=files)
    result = response.json()
    print(f"Pages: {result['metadata']['pageCount']}")
    print(f"Text length: {len(result['text'])}")
```

### cURL
```bash
# Health check
curl http://localhost:8000/health

# Process PDF
curl -X POST \
  -F "file=@document.pdf" \
  http://localhost:8000/process-pdf
```

### JavaScript (fetch)
```javascript
// Process PDF
const formData = new FormData();
formData.append('file', pdfFile); // pdfFile is a File object

fetch('http://localhost:8000/process-pdf', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Pages:', data.metadata.pageCount);
  console.log('Text length:', data.text.length);
  console.log('Images found:', data.images.length);
});
```

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid file format)
- **500**: Internal Server Error (processing failed)

Error responses include details:
```json
{
  "detail": "Error message describing the issue"
}
```

## Deployment

### Local Development
```bash
python api_server.py
```

### Production (using Gunicorn)
```bash
pip install gunicorn
gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker
```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Testing

Run the test script:
```bash
python test_api.py
```

Make sure to replace `sample.pdf` in the test script with the path to an actual PDF file.
