# 📄 AI PDF Chatbot

An AI-powered PDF chatbot that allows users to upload a PDF document and ask questions about its content.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from the uploaded PDF and uses **Google Gemini** to generate a natural-language answer based only on the retrieved context.

## 🚀 Features

- 📤 Upload PDF documents
- 📖 Extract text from PDF pages
- ✂️ Split documents into smaller chunks
- 🧠 Generate semantic embeddings using Sentence Transformers
- 🔎 Perform similarity search using FAISS
- 🤖 Generate answers using Google Gemini
- 📚 Display source pages used for the answer
- 🗑️ Clear the uploaded PDF
- 🔐 Secure uploaded filenames
- 🌐 Simple web interface using Flask, HTML, CSS and JavaScript

## 🧠 How RAG Works

The application follows this pipeline:

```text
PDF Upload
    ↓
PDF Text Extraction
    ↓
Text Chunking
    ↓
Sentence Transformer Embeddings
    ↓
FAISS Vector Store
    ↓
User Question
    ↓
Question Embedding
    ↓
Similarity Search
    ↓
Relevant PDF Chunks
    ↓
Google Gemini
    ↓
Final Answer + Sources
```

Instead of sending the entire PDF to the language model, the application first retrieves the most relevant sections of the document.

This makes the chatbot more focused on the uploaded document and helps reduce hallucinations.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| Google Gemini | Answer generation |
| HTML | Web page structure |
| CSS | User interface styling |
| JavaScript | Frontend interaction |
| python-dotenv | Environment variable management |

## 📁 Project Structure

```text
AI_PDF_Chatbot/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── utils/
│   ├── chatbot.py
│   ├── embeddings.py
│   ├── pdf_processor.py
│   └── vector_store.py
│
├── app.py
├── test_pdf.py
├── test_embeddings.py
├── test_vector_store.py
├── test_rag.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/manojkumarc799/AI_PDF_Chatbot.git
cd AI_PDF_Chatbot
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Gemini API Key Setup

Create a Gemini API key using Google AI Studio.

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not share your API key or commit the `.env` file to GitHub.

## ▶️ Run the Application

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the Flask application:

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## 💬 Example Usage

1. Open the application.
2. Select a PDF document.
3. Click **Upload PDF**.
4. Wait for the document to be processed.
5. Enter a question about the PDF.
6. Click **Ask**.
7. The chatbot retrieves relevant sections and generates an answer.
8. The relevant source pages are displayed.

Example questions:

```text
What is this document about?

What are the main requirements?

Summarize the important points.

What are the key steps mentioned in the document?

Which topics are discussed in the document?
```

## 🧪 Testing

The project includes separate test files for the major components.

### Test PDF extraction

```bash
python test_pdf.py
```

### Test embeddings

```bash
python test_embeddings.py
```

### Test FAISS vector search

```bash
python test_vector_store.py
```

### Test complete RAG pipeline

```bash
python test_rag.py
```

## 🔐 Security

The project uses:

- Environment variables for the Gemini API key
- `secure_filename()` for uploaded filenames
- `.gitignore` to prevent sensitive/generated files from being committed

The following files/directories are intentionally excluded from Git:

```text
.env
.venv/
uploads/
vector_store/
__pycache__/
```

## 🔮 Future Improvements

Possible future enhancements include:

- Conversation history
- Multiple PDF support
- PDF preview
- Streaming Gemini responses
- Better chunking strategies
- Hybrid search using keyword + semantic search
- Persistent vector databases
- User authentication
- Deployment to a cloud platform
- Improved chat-style interface

## 👨‍💻 Author

**Manoj Kumar Daram**

GitHub:  
https://github.com/manojkumarc799

## 📜 License

This project is intended for educational and portfolio purposes.