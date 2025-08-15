# Streamlit PDF Processor

This project is a Streamlit application that allows users to upload PDF files and receive the extracted data in JSON format. The application processes the uploaded PDF files and displays the results in a user-friendly interface.

## Project Structure

```
streamlit-pdf-processor
├── src
│   ├── app.py                # Main entry point for the Streamlit application
│   ├── components
│   │   ├── __init__.py       # Initializes the components package
│   │   ├── file_upload.py     # Handles file upload functionality
│   │   └── json_display.py     # Displays JSON data in a formatted manner
│   ├── services
│   │   ├── __init__.py       # Initializes the services package
│   │   └── pdf_processor.py    # Processes PDF files and extracts data
│   └── utils
│       ├── __init__.py       # Initializes the utils package
│       └── helpers.py         # Contains helper functions for various tasks
├── static
│   └── style.css             # Custom CSS styles for the Streamlit application
├── requirements.txt          # Lists project dependencies
├── config.py                 # Configuration settings for the application
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit-pdf-processor
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```

4. Open your web browser and navigate to `http://localhost:8501` to access the application.

## Usage

- Upload a PDF file using the file uploader.
- The application will process the PDF and display the extracted data in JSON format.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.