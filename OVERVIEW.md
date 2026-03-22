# AI Engineering Bootcamp Project Overview

This repository contains the projects and exercises developed during the AI Engineering Bootcamp. The project is split into two main components: a FastAPI service for text processing and a RAG-powered Q&A system for document analysis.

---

## 📁 Project Structure

### 1. `app/` (FastAPI Text Processing Service)
The `app/` folder contains a production-style FastAPI service designed to demonstrate various LLM prompting strategies for common NLP tasks.

-   **`main.py`**: The entry point for the FastAPI application, handling CORS, loading environment variables, and routing.
-   **`app/llm.py`**: A wrapper for the OpenAI API, managing model selection and chat completions.
-   **`app/routes/`**: Contains the API endpoint definitions:
    -   `health.py`: Simple health check endpoint.
    -   `summarize.py`: Logic for text summarization.
    -   `sentiment.py`: Logic for sentiment analysis.
-   **`app/prompts/`**: Houses the core prompt engineering logic, implementing four strategy types: `zero-shot`, `few-shot`, `chain-of-thought`, and `meta`.

### 2. `rag-powered-q&a-system/` (Document Q&A System)
This folder contains a Retrieval-Augmented Generation (RAG) system built with LangChain, designed to answer technical questions from PDF documents.

-   **`build-your-own-q&a.ipynb`**: The primary interactive notebook for running the RAG pipeline, including ingestion, indexing, and retrieval.
-   **`documents/`**: A storage folder for the raw PDF documents (e.g., product guides) used as the knowledge base.
-   **`rag_vector_db/`**: A persistent ChromaDB storage directory where document embeddings and metadata are saved.
-   **`observations.md`**: A detailed log of performance metrics, chunking experiments, and next steps for the RAG system.
-   **`README.md`**: Technical documentation specific to the RAG architecture, including the Mermaid diagram of the retrieval flow.

---

## 🛠 Tech Stack Summary

-   **API Framework**: FastAPI
-   **LLM Orchestration**: LangChain
-   **Models**: OpenAI GPT-4o-mini, GPT-3.5-turbo, and Text Embedding-3-small.
-   **Vector Database**: ChromaDB
-   **Search Algorithms**: Hybrid Search (Vector Similarity + BM25 Keyword Search).
-   **Deployment**: Render (configured via `render.yaml`).
