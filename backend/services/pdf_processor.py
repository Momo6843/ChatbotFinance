import pdfplumber

def extract_pages(pdf_file):
    pages = []
    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({"page_number": i+1, "text": text})
    return pages

def chunk_pages(pages, chunk_size=3):
    chunks = []
    for i in range(0, len(pages), chunk_size):
        text_chunk = "\n".join([p['text'] for p in pages[i:i+chunk_size]])
        page_numbers = [p['page_number'] for p in pages[i:i+chunk_size]]
        chunks.append({"text": text_chunk, "pages": page_numbers})
    return chunks
