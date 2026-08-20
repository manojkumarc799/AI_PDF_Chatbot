import os

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from utils.pdf_processor import extract_text_from_pdf, create_chunks
from utils.embeddings import create_embeddings
from utils.vector_store import create_vector_store, search_vector_store
from utils.chatbot import generate_answer


app = Flask(__name__)


# Store the currently uploaded PDF data in memory
pdf_chunks = None
vector_index = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():

    global pdf_chunks
    global vector_index

    # Check if a PDF was uploaded
    if "pdf" not in request.files:
        return jsonify({
            "error": "No PDF file uploaded."
        }), 400

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({
            "error": "No PDF file selected."
        }), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "error": "Only PDF files are allowed."
        }), 400

    filename = secure_filename(file.filename)

    if not filename:
        return jsonify({
            "error": "Invalid filename."
        }), 400

    # Make sure uploads directory exists
    os.makedirs("uploads", exist_ok=True)

    # Save PDF
    pdf_path = os.path.join(
        "uploads",
        filename
    )

    file.save(pdf_path)

    # Extract text
    pages = extract_text_from_pdf(pdf_path)

    if not pages:
        return jsonify({
            "error": "Could not extract text from this PDF."
        }), 400

    # Create chunks
    pdf_chunks = create_chunks(pages)

    # Create embeddings
    texts = [
        chunk["text"]
        for chunk in pdf_chunks
    ]

    embeddings = create_embeddings(texts)

    # Create FAISS index
    vector_index = create_vector_store(
        embeddings
    )

    return jsonify({
        "message": "PDF uploaded successfully.",
        "filename": file.filename,
        "pages": len(pages),
        "chunks": len(pdf_chunks)
    })


@app.route("/ask", methods=["POST"])
def ask_question():

    global pdf_chunks
    global vector_index

    # Make sure a PDF has been uploaded
    if pdf_chunks is None or vector_index is None:
        return jsonify({
            "error": "Please upload a PDF first."
        }), 400

    # Get question
    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "error": "Please enter a question."
        }), 400

    # Create question embedding
    query_embedding = create_embeddings(
        [question]
    )

    # Search FAISS
    distances, indices = search_vector_store(
        vector_index,
        query_embedding,
        top_k=3
    )

    # Collect relevant chunks
    retrieved_chunks = []

    sources = []

    for index_number in indices:

        chunk = pdf_chunks[index_number]

        retrieved_chunks.append(
            f"Page {chunk['page']}:\n"
            f"{chunk['text']}"
        )

        sources.append(
            chunk["page"]
        )

    # Combine context
    context = "\n\n".join(
        retrieved_chunks
    )

    # Generate Gemini answer
    answer = generate_answer(
        question,
        context
    )

    return jsonify({
        "answer": answer,
        "sources": sources
    })


@app.route("/clear", methods=["POST"])
def clear_pdf():

    global pdf_chunks
    global vector_index

    # Clear the current PDF data
    pdf_chunks = None
    vector_index = None

    return jsonify({
        "message": "PDF cleared successfully."
    })



if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )