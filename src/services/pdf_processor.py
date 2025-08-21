def process_pdf(pdf_file):
    import fitz  # PyMuPDF
    import json
    import base64
    import hashlib
    from io import BytesIO
    from PIL import Image

    result = {
        "text": "",
        "metadata": {},
        "images": []
    }

    try:
        # Handle both file path strings and Streamlit UploadedFile objects
        if hasattr(pdf_file, 'read'):
            # It's a Streamlit UploadedFile object
            pdf_bytes = pdf_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        else:
            # It's a file path string
            doc = fitz.open(pdf_file)
        
        page_count = len(doc)
        result["metadata"]["pageCount"] = page_count
        
        # Extract additional metadata
        metadata = doc.metadata
        result["metadata"].update({
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "creationDate": metadata.get("creationDate", ""),
            "modificationDate": metadata.get("modDate", "")
        })

        # Extract text
        text_content = []
        for page in doc:
            text_content.append(page.get_text())
        result["text"] = "\n".join(text_content)

        # Extract images
        # Use a set to track duplicate images
        seen_hashes = set()
        
        for page in doc:
            image_list = page.get_images(full=True)
            for img in image_list:
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Hash the image bytes to detect duplicates
                    img_hash = hashlib.sha256(image_bytes).hexdigest()
                    if img_hash in seen_hashes:
                        continue  # skip duplicate
                    seen_hashes.add(img_hash)
                    
                    image = Image.open(BytesIO(image_bytes))
                    buffered = BytesIO()
                    image.convert("RGB").save(buffered, format="JPEG", quality=70)
                    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    result["images"].append(f"data:image/jpeg;base64,{img_base64}")
                except Exception as e:
                    # Skip problematic images
                    continue

        return json.dumps(result)

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        if 'doc' in locals():
            doc.close()