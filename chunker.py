import pdfplumber
import io

def extract_chunks(file_bytes, chunk_size=1000, overlap=100):
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        full_text = " ".join([page.extract_text() or "" for page in pdf.pages])

    words = full_text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks