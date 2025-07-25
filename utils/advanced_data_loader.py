import os
import mimetypes
import pandas as pd

def load_data(file_name, columns=None, sheet_name=None, chunk_size=None):
    file_path = os.path.join('data', file_name) if not os.path.isabs(file_name) else file_name
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    mime, _ = mimetypes.guess_type(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    result = {}

    # Metadata extraction
    result['metadata'] = {
        'file_name': os.path.basename(file_path),
        'size_bytes': os.path.getsize(file_path),
        'mime_type': mime,
        'extension': ext
    }

    # CSV
    if ext == '.csv':
        if chunk_size:
            reader = pd.read_csv(file_path, usecols=columns, chunksize=chunk_size)
            result['data'] = next(reader)
        else:
            result['data'] = pd.read_csv(file_path, usecols=columns)
        return result
    # Excel
    elif ext in ['.xlsx', '.xls']:
        result['data'] = pd.read_excel(file_path, usecols=columns, sheet_name=sheet_name)
        return result
    # JSON
    elif ext == '.json':
        result['data'] = pd.read_json(file_path)
        return result
    # TXT
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        result['data'] = pd.DataFrame({'text': lines})
        return result
    # PDF (text and table extraction)
    elif ext == '.pdf':
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
            result['data'] = pd.DataFrame({'text': [text]})
        except ImportError:
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    text = '\n'.join(page.extract_text() or '' for page in reader.pages)
                result['data'] = pd.DataFrame({'text': [text]})
            except Exception:
                result['error'] = 'PDF support requires pdfplumber or PyPDF2'
        # Table extraction
        try:
            import camelot
            tables = camelot.read_pdf(file_path, pages='all')
            result['tables'] = [t.df for t in tables]
        except Exception:
            result['tables'] = []
        return result
    # Images (OCR)
    elif ext in ['.png', '.jpg', '.jpeg']:
        try:
            import pytesseract
            from PIL import Image
            text = pytesseract.image_to_string(Image.open(file_path))
            result['data'] = pd.DataFrame({'text': [text]})
        except Exception:
            result['error'] = 'OCR support requires pytesseract and Pillow'
        return result
    else:
        result['error'] = f'Unsupported file format: {ext}'
        return result
