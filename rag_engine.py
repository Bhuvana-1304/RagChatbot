from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai

class RAGEngine:
    def __init__(self):
        self.docs = []
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.db = None
        self.retriever = None
        self.uploaded_files = []

        # Put your real Gemini API key here
        api_key = "AIzaSyC4-idS_JcR4OZScXFzoZpSAK758Z_Edv8"  # <--- Replace with your actual Gemini API key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-pro')

    def add_document(self, text, name):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_text(text)
        if not self.db:
            self.db = Chroma.from_texts(
                chunks,
                self.embeddings,
                collection_name="pdf_rag_store",
                persist_directory="./chroma_db"
            )
        else:
            self.db.add_texts(chunks)
        self.retriever = self.db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        self.uploaded_files.append(name)
        print(f"✓ Added document: {name} -> {len(chunks)} chunks")
        return len(chunks)

    def query(self, question):
        if not self.retriever:
            return "No documents uploaded yet."
        try:
            docs = self.retriever.invoke(question)
            if not docs:
                return "No relevant info found in the PDFs."
            context = "\n\n".join([f"[Excerpt {i+1}]: {doc.page_content}" for i, doc in enumerate(docs)])
            prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided context from PDF documents.

Context from uploaded PDFs:
{context}

Question: {question}

Instructions:
- Answer using ONLY the provided context above.
- If the answer is not in the context, say "I don't have enough information in the uploaded PDFs."
- Be concise.

Answer:"""
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
