import pymupdf


def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of a PDF.
    """

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        if text.strip():
            pages.append({
                "page": page_number + 1,
                "text": text.strip()
            })

    document.close()

    return pages


def create_chunks(pages, chunk_size=1000, overlap=200):
    """
    Split extracted PDF text into smaller chunks.
    """

    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "page": page_number,
                    "text": chunk_text.strip()
                })

            start += chunk_size - overlap

    return chunks