# 🟢 Week 8 — Inventory Chatbot API (RAG Integration)
## 📖 Project Overview

Week 8 focuses on integrating AI into the inventory management system by building a Retrieval-Augmented Generation (RAG) pipeline.

## Key objectives:

Understand Large Language Models (LLMs), text embeddings, and vector similarity.

Build a RAG-based chatbot for querying product inventory.

Integrate the RAG pipeline with a Flask API.

Apply secure endpoints using JWT authentication.

By the end of this week, users can ask natural language questions about products and receive context-aware answers.

## ⚙️ Prerequisites

Python 3.11+

PostgreSQL (with pgvector extension enabled)

Virtual environment (venv) recommended

OpenAI API key

## 🛠️ Setup Instructions

Clone the repository
```
git clone <repo-url>
cd inventory-manager
```

Create and activate virtual environment
```
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

```
Install dependencies
```
pip install -r requirements.txt
```

Configure environment variables

Copy .env.example to .env

Set required variables:
```
OPENAI_API_KEY=<your_openai_api_key>
DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db
```

Setup PostgreSQL database

Ensure pgvector extension is installed:
```
CREATE EXTENSION IF NOT EXISTS vector;
```

Run migrations to create tables:
```
flask db upgrade
```

🚀 Running the Application
Start Flask API
inside Week8
```
export FLASK_APP=api.app
flask run
or
python Week8/api/app.py
```

API runs at http://127.0.0.1:5000/ (default)

JWT-protected endpoints are available.

Chat Endpoint

POST /chat/inventory
```
Request Body:

{
  "question": "Which products are low in stock?"
}


Response:

{
  "answer": "The top low-stock products are: ..."
}

```
The endpoint uses the RAG pipeline to retrieve relevant product data and generate a context-aware answer.

## 🔄 RAG Pipeline Workflow

1. Load product data from database.

2. Split data into chunks and generate embeddings using OpenAI.

3. Store embeddings in a PGVector column.

4. Build a LangChain RAG chain:

5. PGVector retriever → Prompt → LLM → Output parser

6. Integrate the RAG chain with Flask endpoint /chat/inventory.

7. Handle JWT authentication with @jwt_required.

## 💻 Key Scripts

| Script              | Purpose                                      |
| ------------------- | -------------------------------------------- |
| `rag_pipeline.py`   | Orchestrates the RAG process end-to-end      |
| `embedding.py`      | Generates embeddings for text data           |
| `data_loader.py`    | Loads and preprocesses product data from CSV |
| `rag_chain.py`      | Constructs the LangChain RAG chain           |
| `db_utils.py`       | Database helper utilities                    |
| `cost_calculate.py` | Calculates OpenAI API cost based on tokens   |
| `system_prompt.py`  | Stores system prompt template for LLM        |


## 🎯 Learning Outcomes

Build a RAG-powered Flask API.

Work with vector databases and embeddings.

Apply LangChain abstractions to connect LLMs with structured data.

Integrate AI features into an existing product inventory system.
