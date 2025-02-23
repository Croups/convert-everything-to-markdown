# MarkItDown Converter

A Streamlit-based web application that converts various document formats to Markdown with AI-powered image descriptions.

## Features

- Supports multiple file formats:
  - PDF documents
  - Word documents (DOC, DOCX)
  - Excel spreadsheets (XLS, XLSX)
  - PowerPoint presentations (PPT, PPTX)
  - Images (JPG, PNG, etc.)
  - HTML files
  - Text-based formats (CSV, JSON, XML)
  - ZIP files (iterates over every file)

- AI Integration:
  - OpenAI GPT-4 Vision for image descriptions
  - Intelligent content extraction

- User Interface:
  - Dark mode support
  - Drag-and-drop file upload
  - Real-time conversion progress
  - Preview converted content
  - Individual and combined file downloads

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Croups/convert-everything-to-markdown.git
cd convert-everything-to-markdown
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Using the application:
   - Enter your OpenAI API key (required for image descriptions)
   - Upload files using drag-and-drop or file browser
   - Click "Convert Files" to begin processing
   - Download individual files or combined markdown

## Requirements

- Python 3.8 or higher
- OpenAI API key (for image descriptions)
- Required packages:
  ```
  streamlit
  markitdown
  openai
  python-dotenv
  ```

## Project Structure

```
markitdown-converter/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
├── documents/            # Temporary storage for uploaded files
└── converted/            # Output directory for converted files
```

## Troubleshooting

- **File Upload Issues**: Check file size limits (default 200MB)
- **Image Description Failures**: Verify OpenAI API key is correct

## DETAILS

- See details here : https://github.com/microsoft/markitdown

## CONTACT 

- Reach me out from linkedin : www.linkedin.com/in/enes-koşar

