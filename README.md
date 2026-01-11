# RAG-Based Document Question Answering System

A Retrieval-Augmented Generation (RAG) based document assistant that allows users to upload PDF files and ask questions about their content. The system uses embeddings, vector search (FAISS), and a locally hosted LLM (Ollama) to generate accurate, context-aware responses in real time with token streaming.

---

## 🚀 Features

- PDF document upload
- Text chunking and preprocessing
- Embedding generation
- FAISS-based vector similarity search
- Retrieval-Augmented Generation (RAG)
- Local LLM integration using Ollama
- Real-time token streaming
- FastAPI backend
- Single-page web UI
- Chat-style interface
- Dark mode UI
- Automatic scrolling
- End-to-end pipeline: Upload → Index → Retrieve → Generate

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- LangChain
- FAISS
- Ollama (local LLM)
- HuggingFace Embeddings

### Frontend
- HTML
- CSS
- Vanilla JavaScript

### Machine Learning / NLP
- Embeddings
- Vector similarity search
- Chunking strategies
- Retrieval-Augmented Generation (RAG)

---

## 🧠 System Architecture

User
↓
Web UI
↓
FastAPI Backend
↓
PDF Ingestion → Chunking → Embeddings → FAISS Index
↓
User Query → Similarity Search → Context Retrieval
↓
Prompt Construction
↓
Local LLM (Ollama)
↓
Streaming Response to UI

yaml
Copy code

---

## ⚙️ How It Works

1. The user uploads a PDF document.
2. The document is split into smaller chunks.
3. Each chunk is converted into vector embeddings.
4. The embeddings are stored in a FAISS vector database.
5. When a user asks a question:
   - The query is embedded.
   - Relevant chunks are retrieved using vector similarity search.
   - These chunks are injected into the LLM prompt.
   - The LLM generates a context-aware response.
6. The response is streamed token-by-token to the UI.

---

## 📂 Folder Structure

rag-document-assistant/
│
├── src/
│ ├── app.py
│ ├── ingest.py
│ ├── retrieve.py
│ ├── generate.py
│
├── data/
│ └── docs/
│
├── vector_store/
├── requirements.txt
└── README.md

yaml
Copy code

---

## 🧪 Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd rag-document-assistant
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
Install dependencies:

bash
Copy code
pip install -r requirements.txt
▶️ Running the Application
1. Start Ollama
bash
Copy code
ollama serve
Pull a model:

bash
Copy code
ollama pull llama2
2. Start the FastAPI Server
bash
Copy code
uvicorn src.app:app --reload
3. Open in Browser
cpp
Copy code
http://127.0.0.1:8000
🎯 Use Case
This system allows users to:

Upload large PDF documents

Ask natural language questions

Receive accurate, context-aware answers

Get responses in real time via token streaming

Interact with a chat-style UI

🔮 Future Improvements
Source citation display

Chat memory

Markdown rendering

Multi-document support

Drag-and-drop upload

Authentication

Cloud deployment

💡 Why This Project Matters
This project demonstrates:

End-to-end RAG pipeline implementation

Working with vector databases

Local LLM deployment

Backend API design

Real-time streaming systems

Practical AI system design

Debugging real-world ML pipelines