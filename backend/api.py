from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os
import shutil
import logging
from model import RAGModel
from typing import List, Optional, Dict, Any

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Question(BaseModel):
    text: str

class Answer(BaseModel):
    answer: str
    status: str
    sources: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

# Initialize model with environment variables
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
documents_dir = os.getenv("DOCUMENTS_DIR", "/app/documents")

# Ensure documents directory exists
os.makedirs(documents_dir, exist_ok=True)

logger.info(f"Using DOCUMENTS_DIR: {documents_dir}")
logger.info(f"Using OLLAMA_URL: {ollama_url}")

model = RAGModel(data_dir=documents_dir, base_url=ollama_url)

@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup."""
    try:
        # Load documents and initialize QA chain
        model.load_and_process_documents()  # Removed 'await'
        model.initialize_qa_chain()
        logger.info("Model initialization completed")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to the documents directory."""
    try:
        file_path = os.path.join(documents_dir, file.filename)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        logger.info(f"File uploaded successfully: {file_path}")

        # Re-process the documents after upload
        model.load_and_process_documents()  # Removed 'await'

        return {"message": "File uploaded successfully", "file_path": file_path}
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return {"error": str(e)}


@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    """Handle questions and return answers."""
    try:
        result = model.get_answer(question.text)
        sources_metadata = []

        if result["sources"]:
            for doc in result["sources"]:
                sources_metadata.append(doc.metadata)  # Extract metadata

        return Answer(
            answer=result["answer"],
            status=result["status"],
            sources=sources_metadata,  # Return serialized metadata
            error=result.get("error")
        )
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return Answer(
            answer="An error occurred",
            status="error",
            error=str(e)
        )
