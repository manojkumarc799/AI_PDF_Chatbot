from utils.pdf_processor import extract_text_from_pdf, create_chunks
from utils.embeddings import create_embeddings
from utils.vector_store import create_vector_store, search_vector_store


pdf_path = "uploads/My ATS Friendly Resume.pdf"


# 1. Extract PDF text
pages = extract_text_from_pdf(pdf_path)


# 2. Create chunks
chunks = create_chunks(pages)


# 3. Create embeddings
texts = [chunk["text"] for chunk in chunks]

embeddings = create_embeddings(texts)


# 4. Create FAISS vector store
index = create_vector_store(embeddings)


print("Number of chunks:", len(chunks))
print("FAISS vectors:", index.ntotal)
print("Vector dimension:", index.d)


# 5. Test a question
question = "What programming related coursework is mentioned?"


# Convert question into an embedding
query_embedding = create_embeddings([question])


# Search FAISS
distances, indices = search_vector_store(
    index,
    query_embedding,
    top_k=3
)


print("\nQuestion:", question)

print("\nMost relevant chunks:")

for distance, index_number in zip(distances, indices):

    chunk = chunks[index_number]

    print("\n-------------------------")
    print("Page:", chunk["page"])
    print("Distance:", distance)
    print("Text:")
    print(chunk["text"])