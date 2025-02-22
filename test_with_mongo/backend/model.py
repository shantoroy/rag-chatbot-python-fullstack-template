from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any
import logging
import os
import gridfs
import base64
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGModel:
    def __init__(self, mongodb_url: str, ollama_url: str = "http://localhost:11434"):
        """
        Initialize the RAG model with necessary components.
        
        Args:
            mongodb_url (str): URL for MongoDB connection
            ollama_url (str): URL for local Ollama service
        """
        # MongoDB setup
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client.company_docs
        self.fs = gridfs.GridFS(self.db)
        
        # Initialize embeddings model
        logger.info("Initializing embedding model...")
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=ollama_url
        )
        
        # Initialize LLM
        logger.info("Initializing LLM...")
        self.llm = Ollama(
            model="mistral",
            base_url=ollama_url,
            temperature=0.1
        )
        
        self.vector_store = None
        self.qa_chain = None

    async def process_pdf(self, file_id: str) -> None:
        """Process a PDF file from MongoDB and update the vector store."""
        try:
            # Retrieve file from GridFS
            grid_out = await self.db.fs.files.find_one({"_id": file_id})
            if not grid_out:
                raise ValueError(f"File {file_id} not found")

            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                # Write GridFS file to temp file
                chunks = self.fs.get(file_id)
                temp_file.write(chunks.read())
                temp_file_path = temp_file.name

            # Load and process PDF
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
            )
            texts = text_splitter.split_documents(documents)

            # Update or create vector store
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(texts, self.embeddings)
            else:
                self.vector_store.add_documents(texts)

            # Clean up temp file
            os.unlink(temp_file_path)
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise

    async def initialize_from_mongodb(self) -> None:
        """Initialize vector store from all documents in MongoDB."""
        try:
            # Get all file IDs from GridFS
            cursor = self.db.fs.files.find()
            async for doc in cursor:
                await self.process_pdf(doc['_id'])

            if self.vector_store:
                self.initialize_qa_chain()
                
        except Exception as e:
            logger.error(f"Error initializing from MongoDB: {str(e)}")
            raise

    def initialize_qa_chain(self) -> None:
        """Initialize the question-answering chain."""
        try:
            if not self.vector_store:
                raise ValueError("Vector store not initialized")

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": 3}
                ),
            )
            
        except Exception as e:
            logger.error(f"Error initializing QA chain: {str(e)}")
            raise

    async def get_answer(self, question: str) -> Dict[str, Any]:
        """Get answer for a given question."""
        try:
            if not self.qa_chain:
                raise ValueError("QA chain not initialized")

            result = self.qa_chain({"query": question})
            
            return {
                "answer": result["result"],
                "sources": result.get("source_documents", []),
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error getting answer: {str(e)}")
            return {
                "answer": "Sorry, I encountered an error processing your question.",
                "error": str(e),
                "status": "error"
            }