# 🔮 Enterprise RAG System

A production-style Retrieval-Augmented Generation (RAG) system built using **Python**, **Streamlit**, **FAISS**, **BM25**, **Ollama**, and modern retrieval techniques.

This project enables users to upload PDF documents, build a searchable knowledge base, and chat with their documents using a local Large Language Model (LLM).

---

## ✨ Features

### 📚 Knowledge Base Management

- PDF document ingestion
- Knowledge base rebuilding
- Replace existing documents with new datasets
- Persistent document storage
- Automatic indexing pipeline

### 🔍 Advanced Retrieval

- FAISS Vector Search
- BM25 Lexical Search
- Hybrid Retrieval (FAISS + BM25)
- Configurable Top-K Retrieval

### 🧠 Advanced RAG Features

- Query Rewriting
- Cross-Encoder Reranking
- Conversational Memory
- Source Attribution
- Multi-document Retrieval

### 🤖 LLM Integration

- Ollama-based local inference
- Configurable model selection
- Adjustable conversation history

### 🎨 Modern UI

- Interactive Streamlit Dashboard
- Knowledge Base Management
- Configuration Panel
- Chat Interface
- Source Citations

---

# 🏗️ System Architecture

```text
                ┌─────────────┐
                │    PDFs     │
                └──────┬──────┘
                       │
                       ▼
              ┌────────────────┐
              │ PDF Extraction │
              └──────┬─────────┘
                     │
                     ▼
             ┌───────────────┐
             │ Chunking      │
             └──────┬────────┘
                    │
                    ▼
            ┌─────────────────┐
            │ Embeddings      │
            └──────┬──────────┘
                   │
                   ▼
         ┌───────────────────────┐
         │ Vector Store (FAISS)  │
         └─────────┬─────────────┘
                   │
                   ▼
              User Query
                   │
                   ▼
          Query Rewriting
                   │
                   ▼
          Document Retrieval
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
      FAISS              BM25
          │                 │
          └──────┬──────────┘
                 ▼
          Hybrid Results
                 │
                 ▼
             Reranker
                 │
                 ▼
           Context Builder
                 │
                 ▼
                LLM
                 │
                 ▼
            Final Answer
```

---

# 📁 Project Structure

```text
project/
│
├── streamlit_app.py
│
├── config/
│   ├── config.json
│   └── config_loader.py
│
├── RAG/
│   └── rag.py
│
├── retrievers/
│   ├── faiss_retriever.py
│   ├── bm25_retriever.py
│   └── hybrid_retriever.py
│
├── vector_store/
│   └── vector_store.py
│
├── data/
│   └── uploads/
│
├── embeddings/
│
└── requirements.txt
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone <repository_url>
cd enterprise-rag
```

## Create Virtual Environment

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Ollama Setup

Install Ollama:

https://ollama.com

Pull a model:

```bash
ollama pull qwen2.5:3b
```

or

```bash
ollama pull llama3.2
```

Verify installation:

```bash
ollama list
```

Start Ollama:

```bash
ollama serve
```

---

# ▶️ Running the Application

```bash
streamlit run streamlit_app.py
```

Application will be available at:

```text
http://localhost:8501
```

---

# 📚 Building the Knowledge Base

1. Open the Configuration page.
2. Upload PDF documents.
3. Click **Replace & Rebuild Knowledge Base**.
4. Wait for indexing to complete.
5. Open the Chat page.
6. Start asking questions.

---

# ⚙️ Configuration

## Chunking

| Parameter | Description |
|------------|------------|
| Chunk Size | Tokens per chunk |
| Chunk Overlap | Overlap between chunks |

## Retrieval

| Parameter | Description |
|------------|------------|
| Retriever Type | FAISS / BM25 / Hybrid |
| Top K | Number of retrieved chunks |

## Query Rewriting

Improves retrieval quality by reformulating user queries using conversation context.

## Reranking

Uses a cross-encoder model to improve retrieval precision by reordering retrieved chunks.

## Conversation History

Controls how many previous interactions are included in the prompt.

---

# 🔎 Retrieval Methods

## FAISS

Semantic vector search using embeddings.

**Best for:**

- Meaning-based search
- Concept retrieval
- Semantic similarity

## BM25

Keyword-based retrieval.

**Best for:**

- Exact terminology
- Technical keywords
- Acronyms

## Hybrid Retrieval

Combines:

- FAISS
- BM25

Recommended for most use cases because it balances recall and precision.

---

# 📖 Source Attribution

Each generated response includes:

- Source document name
- Page range

This improves transparency and allows users to verify answers.

---

# 💬 Example Workflow

### Upload Documents

```text
employee_handbook.pdf
company_policy.pdf
architecture_guide.pdf
```

### Build Knowledge Base

```text
Chunking
→ Embeddings
→ Index Creation
→ Retrieval Ready
```

### Ask a Question

```text
What is the leave policy?
```

### System Processing

```text
Query Rewriting
→ Retrieval
→ Reranking
→ Context Construction
→ LLM Generation
```

### Output

```text
Answer + Source Citations
```

---

# 🛠️ Tech Stack

- Python
- Streamlit
- Ollama
- FAISS
- BM25
- Sentence Transformers
- PyMuPDF
- NumPy
- Scikit-Learn

---

# 🔮 Future Improvements

- Multi-user support
- Role-based access control
- Metadata filtering
- Incremental indexing
- Knowledge graph integration
- Agentic RAG
- Citation highlighting
- Document versioning
- Web document ingestion
- Streaming responses

---