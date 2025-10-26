
# RAG PDF Chatbot

A powerful Retrieval-Augmented Generation (RAG) chatbot that answers user questions using the content of uploaded PDFs, with Google Gemini as the LLM.

***

## Workflow (How it Works)

**PDF Upload & Extraction**
- User uploads multiple PDFs via a web UI.
- Text is extracted from each PDF using `pdfminer.six` and `pymupdf`.
  - Both are chosen for their reliability and Python compatibility.

**Text Chunking**
- Extracted text is split into small, meaningful chunks by LangChain’s text splitter.
  - Chunking is critical: LLMs work best with well-bounded, contextually complete passages.

**Embedding & Storage**
- Each chunk is converted into a semantic vector using **all-MiniLM-L6-v2** via `langchain-huggingface`.
  - This model is fast and proven for retrieval tasks, balancing speed and accuracy well.
- Embeddings are stored in ChromaDB—chosen for its open-source, fast, local similarity search.

**Query Processing**
- The user submits a question via the chat interface.
- The app retrieves the most similar text chunks from all PDFs using vector similarity searching (ChromaDB).
  - This ensures answers are always grounded in the user’s documents.

**Answer Generation with Gemini**
- Retrieved context is sent to Gemini (`models/gemini-2.5-pro`) using Google’s SDK.
  - Gemini 2.5 Pro is selected because it’s the newest, most capable, with large context windows, and easy integration via API or SDK.
- Gemini generates the final answer, always limited to only the provided PDF context.

**Serving and API**
- FastAPI handles backend endpoints for all chatbot actions.
  - FastAPI is chosen for its async performance, auto-docs, and beautiful developer experience.
- The simple frontend lets users upload PDF files and chat in their browser.

**Environment Setup**
- Windows + PowerShell is the primary development setup.
  - PowerShell is used for reliable virtual environment activation on Windows.

***

## Technology Choices & Rationale

- **`pdfminer.six` & `pymupdf`**: Robust text extraction even from complex or scanned PDFs.
- **LangChain chunking**: Generates semantically meaningful text segments for better QA accuracy.
- **`all-MiniLM-L6-v2` embeddings**: Chosen for proven speed and accuracy in search applications with limited resources.
- **ChromaDB**: Open source, easy to set up locally, integrates naturally with LangChain and Python apps.
- **Google Gemini 2.5 Pro**: Latest LLM with premier performance for RAG tasks, long context, and enterprise-grade reliability.
- **FastAPI & Uvicorn**: Async, rapid prototyping, and smooth deployment.
- **PowerShell (`.ps1` activation)**: Ensures hassle-free venv activation on Windows machines.

***

## Challenges and How I Addressed Them

- **Model selection errors**: Faced 404 errors when Gemini model names were wrong. Solved by listing supported models using the SDK and using `'models/gemini-2.5-pro'`.
- **Embedding dimension mismatch**: If the embedding model is swapped, ChromaDB may throw dimension errors. Always delete/reset the `chroma_db` folder after such changes.
- **PDF parsing issues**: Some edge-case PDFs might fail to extract. Used alternative libraries and provided clear error messages to users.
- **Infinite reload loops**: VS Code and Windows environments sometimes cause reload storms if `--reload` is used. For stability, use plain `uvicorn main:app`.
- **Environment confusion**: Explicitly documented PowerShell usage to help Windows users avoid venv activation issues.

***

## How to Run (Windows + PowerShell)

1. Open VS Code and navigate to your project folder.
2. Open the VS Code terminal (make sure it's PowerShell).
3. Activate the environment:
    ```
    .\rag_env\Scripts\Activate.ps1
    ```
4. Start the FastAPI server:
    ```
    uvicorn main:app
    ```
5. Open your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000)
6. Upload PDFs and start asking questions!

***

## Why This Approach?

- RAG (Retrieval-Augmented Generation) ensures the chatbot gives factual, context-grounded answers based only on uploaded PDFs, reducing hallucination and improving answer quality.
- Each technology was chosen for its balance of ease of use, support for long-document workflows, and best-in-class performance in open, accessible tools.

***
