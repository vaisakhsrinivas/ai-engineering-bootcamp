# Q & A System Observations

### Problem
Build a Retrieval-Augmented Generation (RAG) Q & A agent using a real-world file/document (The document used in this case is a product guide, specifically the NetWitness UEBA User Guide).

### Implementation Context
The system was built using modern LangChain patterns, utilizing a hybrid search approach (Ensemble Retriever) combining Vector Similarity (ChromaDB) and Keyword-based search (BM25).

### Observations

#### 1. Retrieval Accuracy and Performance
- **Overall Accuracy**: 4/5 for retrieval, faithfulness, and correctness.
- **Retrieval Quality**: The system successfully retrieved the right chunks for most questions, with answers staying within size limits and remaining grounded in the provided context.

#### 2. Chunking Strategy
- Performance significantly varied based on chunk size and overlap.
- **Initial Configuration**: 500 characters with 100 character overlap.
- **Optimized Configuration**: 1000 characters with 300 character overlap.
- **Finding**: Larger chunk sizes (1000/300) provided better context for the LLM, leading to more comprehensive and accurate answers.

#### 3. Hybrid Search Effectiveness
- The combination of **Vector Retriever** (Weight: 0.4) and **BM25 Retriever** (Weight: 0.6) improved results.
- Keyword-based search (BM25) was particularly helpful for specific technical terms found in the product guide, while vector similarity handled semantic queries effectively.

#### 4. Challenges and Data Retrieval Confusion
- **Context Overlap**: When multiple documents were present (e.g., UEBA Guide vs. FIA Regulations), the model occasionally picked up irrelevant context if questions were not specific enough.
- **Hallucination Prevention**: Answers were strictly grounded in context, but specific prompts were needed to ensure the agent cited the correct guide when multiple sources were indexed.
- **Database Persistence**: Clearing the `rag_vector_db` folder was sometimes necessary when switching between significantly different document sets to prevent old embeddings from interfering with new queries.


### Next Steps
Based on current findings, the following areas are identified for further optimization:
- **Improving Chunking Mechanism**: Moving beyond fixed-size chunking to explore semantic chunking or document-aware splitting (e.g., splitting by headers or sections).
- **Multi-Document Variety**: Testing the system with multiple PDFs containing varying data structures (e.g., combining technical manuals, legal documents, and conversational transcripts) to improve retrieval robustness.
- **Adding a User Interface**: Developing a web-based UI (e.g., using Streamlit or Gradio) to make the system accessible to non-technical users.
- **Hybrid Search Tuning**: Experimenting with varying weights for Vector Similarity and BM25 retrievers to find the optimal balance for different document domains.
- **Improved Data Persistence**: Identifying better ways to persist data, as ChromaDB exhibited issues (e.g., needing manual folder clearing) while re-running commands.

### Conclusion
The RAG system is highly effective for technical product guides. Further improvements can be achieved by fine-tuning chunking parameters and retriever weights specific to the document's structure.
