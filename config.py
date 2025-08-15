import os

class Config:
    PDF_PROCESSING_API_URL = os.getenv("PDF_PROCESSING_API_URL", "http://localhost:5000/process-pdf")
    MAX_UPLOAD_SIZE_MB = 50  # Maximum upload size in MB
    ALLOWED_EXTENSIONS = {'pdf'}  # Allowed file extensions for upload

    @staticmethod
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS