def validate_pdf_file(file):
    """
    Validate if the uploaded file is a PDF.
    Returns True if valid, otherwise False.
    """
    return file is not None and file.type == "application/pdf"

def format_json_response(response):
    """
    Format the JSON response for better readability.
    Returns a pretty-printed JSON string.
    """
    import json
    return json.dumps(response, indent=2)