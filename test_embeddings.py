from utils.pdf_processor import extract_text_from_pdf, create_chunks
from utils.embeddings import create_embeddings


pdf_path = "uploads/My ATS Friendly Resume.pdf"


# Extract PDF text
pages = extract_text_from_pdf(pdf_path)

# Create chunks
chunks = create_chunks(pages)


# Extract only the text from each chunk
texts = [chunk["text"] for chunk in chunks]


# Create embeddings
embeddings = create_embeddings(texts)


print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)
print("First embedding:")
print(embeddings[0])