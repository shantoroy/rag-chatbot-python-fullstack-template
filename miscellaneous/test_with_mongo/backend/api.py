from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import gridfs
from bson import ObjectId
from backend.model import RAGModel
import os
from typing import Optional
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Question(BaseModel):
    text: str

class Answer(BaseModel):
    answer: str
    status: str
    error: Optional[str] = None

# Initialize MongoDB and model
mongodb_url = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
model = RAGModel(mongodb_url=mongodb_url, ollama_url=ollama_url)

@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup."""
    try:
        await model.initialize_from_mongodb()
        logger.info("Model initialization completed")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a PDF file to MongoDB."""
    try:
        # Save file to GridFS
        contents = await file.read()
        file_id = await model.db.fs.upload_from_stream(
            file.filename,
            contents
        )
        
        # Process the new file
        await model.process_pdf(file_id)
        
        return {"message": "File uploaded successfully", "file_id": str(file_id)}
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    """Handle questions and return answers."""
    try:
        result = await model.get_answer(question.text)
        return Answer(
            answer=result["answer"],
            status=result["status"],
            error=result.get("error")
        )
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return Answer(
            answer="An error occurred",
            status="error",
            error=str(e)
        )