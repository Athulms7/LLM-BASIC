# 🚀 RAG PDF QA System  
FastAPI + Pinecone + Groq + Celery + Redis

A scalable Retrieval-Augmented Generation (RAG) backend that allows users to:

- 📄 Upload PDFs
- 🧠 Store embeddings in Pinecone (per-user namespace isolation)
- ❓ Ask questions based on uploaded documents
- ⚡ Process uploads asynchronously using Celery + Redis
- 🤖 Generate answers using Groq LLM

---

# 🏗 Architecture Overview
User
↓
FastAPI API
↓
Redis (Message Broker + Result Backend)
↓
Celery Worker (PDF Processing)
↓
Pinecone (Vector Database - Namespace Isolated)
↓
Groq LLM (Answer Generation)

---

# 📁 Project Structure

<details>
<summary>Click to expand</summary>

  .
  ├── app/
  │ ├── init.py
  │ ├── main.py # FastAPI entrypoint
  │ ├── tasks.py # Celery tasks
  │ ├── celery_app.py # Celery configuration
  │ ├── vectorstore.py # Pinecone setup
  │ ├── embeddings.py # Embedding model (singleton)
  │ ├── rag.py # LLM + prompt logic
  │ ├── config.py # Environment variables
  │ └── types.py # Pydantic models
  │
  ├── requirements.txt
  ├── .env.example
  ├── README.md
  └── .gitignore 
  
</details>

---

# 🛠 Prerequisites

- Python 3.10+
- Redis installed (or Docker)
- Pinecone account
- Groq API key

---

# 🔧 Installation Guide

## 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd llm-rag-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Start Redis and Celery
```bash
docker run -p 6379:6379 redis
celery -A app.tasks worker --pool=solo --loglevel=info
```

## Start the Main App
```bash
uvicorn app.main:app --reload
```
