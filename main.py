from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import os
from rag_engine import RAGEngine

app = FastAPI(title="RAG PDF Chatbot API")

# Initialize RAG engine
rag_engine = RAGEngine()

# Directory for uploaded PDFs
UPLOAD_DIR = Path("uploaded_pdfs")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the web interface with correct UTF-8 encoding."""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())
        # Replace this with your own text extraction as needed
        from pdfminer.high_level import extract_text
        text = extract_text(str(file_path))
        chunks_added = rag_engine.add_document(text, file.filename)
        return JSONResponse({
            "message": f"✓ Successfully uploaded {file.filename}",
            "chunks_added": chunks_added,
            "filename": file.filename
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/query")
async def query(question: str = Form(...)):
    """Query the RAG system"""
    try:
        answer = rag_engine.query(question)
        return JSONResponse({"answer": answer, "question": question})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
