from utils.pdf_processor import extract_text_from_pdf, create_chunks
from utils.embeddings import create_embeddings
from utils.vector_store import create_vector_store, search_vector_store
from utils.chatbot import generate_answer


# PDF path
pdf_path = "uploads/My ATS Friendly Resume.pdf"


# ------------------------------------------------
# 1. Extract PDF text
# ------------------------------------------------

pages = extract_text_from_pdf(pdf_path)


# ------------------------------------------------
# 2. Create chunks
# ------------------------------------------------

chunks = create_chunks(pages)


# ------------------------------------------------
# 3. Create embeddings
# ------------------------------------------------

texts = [chunk["text"] for chunk in chunks]

embeddings = create_embeddings(texts)


# ------------------------------------------------
# 4. Create FAISS vector store
# ------------------------------------------------

index = create_vector_store(embeddings)


# ------------------------------------------------
# 5. Ask a question
# ------------------------------------------------

question = "What programming languages are mentioned?"


# ------------------------------------------------
# 6. Convert question into embedding
# ------------------------------------------------

query_embedding = create_embeddings([question])


# ------------------------------------------------
# 7. Search FAISS
# ------------------------------------------------

distances, indices = search_vector_store(
    index,
    query_embedding,
    top_k=3
)


# ------------------------------------------------
# 8. Collect relevant chunks
# ------------------------------------------------

retrieved_chunks = []

for index_number in indices:

    chunk = chunks[index_number]

    retrieved_chunks.append(
        f"Page {chunk['page']}:\n{chunk['text']}"
    )


# ------------------------------------------------
# 9. Combine retrieved chunks
# ------------------------------------------------

context = "\n\n".join(retrieved_chunks)


# ------------------------------------------------
# 10. Ask Gemini
# ------------------------------------------------

answer = generate_answer(
    question,
    context
)


# ------------------------------------------------
# 11. Display result
# ------------------------------------------------

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)

print("\nSOURCES:")

for index_number in indices:
    print(f"Page {chunks[index_number]['page']}")