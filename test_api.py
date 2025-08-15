import requests
import json

def test_pdf_processor_api(pdf_file_path, api_base_url="http://localhost:8000"):
    """
    Test the PDF Processor API
    
    Args:
        pdf_file_path: Path to the PDF file to process
        api_base_url: Base URL of the API (default: http://localhost:8000)
    """
    
    print(f"🔗 Testing PDF Processor API at: {api_base_url}")
    
    # Test health endpoint
    try:
        health_response = requests.get(f"{api_base_url}/health")
        if health_response.status_code == 200:
            print("✅ API Health Check: PASSED")
        else:
            print("❌ API Health Check: FAILED")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        return
    
    # Test PDF processing
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            files = {'file': (pdf_file_path, pdf_file, 'application/pdf')}
            
            print(f"📤 Uploading PDF: {pdf_file_path}")
            response = requests.post(f"{api_base_url}/process-pdf", files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ PDF Processing: SUCCESS")
                print(f"📊 Pages: {result.get('metadata', {}).get('pageCount', 'N/A')}")
                print(f"📝 Text Length: {len(result.get('text', ''))}")
                print(f"🖼️ Images Found: {len(result.get('images', []))}")
                
                # Save result to file
                with open('api_test_result.json', 'w') as f:
                    json.dump(result, f, indent=2)
                print("💾 Full result saved to 'api_test_result.json'")
                
            else:
                print(f"❌ PDF Processing: FAILED (Status: {response.status_code})")
                print(f"Error: {response.text}")
                
    except FileNotFoundError:
        print(f"❌ File not found: {pdf_file_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_metadata_only_api(pdf_file_path, api_base_url="http://localhost:8000"):
    """Test the metadata-only endpoint"""
    
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            files = {'file': (pdf_file_path, pdf_file, 'application/pdf')}
            
            print(f"📤 Testing metadata-only endpoint...")
            response = requests.post(f"{api_base_url}/process-pdf-metadata-only", files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Metadata Extraction: SUCCESS")
                print(f"📊 Metadata: {json.dumps(result['metadata'], indent=2)}")
            else:
                print(f"❌ Metadata Extraction: FAILED (Status: {response.status_code})")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Example usage
    pdf_file = "sample.pdf"  # Replace with your PDF file path
    
    print("=" * 50)
    print("🧪 PDF Processor API Test")
    print("=" * 50)
    
    # Test full processing
    test_pdf_processor_api(pdf_file)
    
    print("\n" + "=" * 50)
    print("🧪 Metadata-Only API Test")
    print("=" * 50)
    
    # Test metadata-only processing
    test_metadata_only_api(pdf_file)
