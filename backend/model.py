from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, UnstructuredMarkdownLoader, UnstructuredFileLoader
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from typing import List, Dict, Any
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGModel:
    def __init__(self, data_dir: str, base_url: str = "http://ollama:11434", vector_store_path: str = "/app/vector_store"):
        """
        Initialize the RAG model with necessary components.
        
        Args:
            data_dir (str): Directory containing company documents.
            base_url (str): URL for Ollama service.
            vector_store_path (str): Path to save/load the FAISS vector store.
        """
        self.data_dir = data_dir
        self.vector_store_path = vector_store_path
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.vector_store_path, exist_ok=True)

        logger.info(f"Using DOCUMENTS_DIR: {self.data_dir}")
        logger.info(f"Using VECTOR_STORE_PATH: {self.vector_store_path}")

        # Initialize embeddings model
        logger.info("Initializing embedding model...")
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=base_url
        )
        
        # Initialize LLM
        logger.info("Initializing LLM...")
        self.llm = Ollama(
            model="mistral",
            base_url=base_url,
            temperature=0.1
        )

        self.vector_store = None
        self.qa_chain = None

    # def load_and_process_documents(self) -> None:
    #     """Load documents from directory and create vector store."""
    #     try:
    #         logger.info("Loading documents from directory...")

    #         # Load PDF, txt, and markdown files
    #         pdf_loader = DirectoryLoader(self.data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
    #         txt_loader = DirectoryLoader(self.data_dir, glob="**/*.txt")
    #         md_loader = DirectoryLoader(self.data_dir, glob="**/*.{md,markdown}", loader_cls=UnstructuredMarkdownLoader)

    #         pdf_documents = pdf_loader.load()
    #         txt_documents = txt_loader.load()
    #         md_documents = md_loader.load()
            
    #         documents = pdf_documents + txt_documents + md_documents
            
    #         if not documents:
    #             logger.warning("No documents found in the directory. Skipping vector store creation.")
    #             return

    #         logger.info(f"Loaded {len(documents)} documents:")
    #         logger.info(f"- PDF files: {len(pdf_documents)}")
    #         logger.info(f"- Text files: {len(txt_documents)}")
    #         logger.info(f"- Markdown files: {len(md_documents)}")

    #         text_splitter = RecursiveCharacterTextSplitter(
    #             chunk_size=1000,
    #             chunk_overlap=200,
    #         )
    #         texts = text_splitter.split_documents(documents)
    #         logger.info(f"Split into {len(texts)} text chunks.")

    #         logger.info("Creating vector store...")
    #         self.vector_store = FAISS.from_documents(texts, self.embeddings)

    #         # Save the vector store for future use
    #         self.save_vector_store()
            
    #     except Exception as e:
    #         logger.error(f"Error processing documents: {str(e)}")
    #         raise

    def load_and_process_documents(self) -> None:
        """Load documents from directory and create vector store."""
        try:
            logger.info("Loading documents from directory...")

            # Load PDF, txt, and markdown files
            pdf_loader = DirectoryLoader(self.data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
            txt_loader = DirectoryLoader(
                self.data_dir,
                glob="**/*.txt",
                loader_cls=UnstructuredFileLoader,
                loader_kwargs={'mode': "single"}
            )
            md_loader = DirectoryLoader(
                self.data_dir, 
                glob="**/*.{md,markdown}", 
                loader_cls=UnstructuredMarkdownLoader,
                loader_kwargs={'mode': "single"}
            )

            pdf_documents = pdf_loader.load()
            logger.info(f"Loaded {len(pdf_documents)} pdf documents")
            txt_documents = txt_loader.load()
            logger.info(f"Loaded {len(txt_documents)} txt documents")
            md_documents = md_loader.load()
            logger.info(f"Loaded {len(md_documents)} markdown documents")

            documents = pdf_documents + txt_documents + md_documents

            if not documents:
                logger.warning("No documents found in the directory. Skipping vector store creation.")
                return

            logger.info(f"Loaded {len(documents)} documents:")
            logger.info(f"- PDF files: {len(pdf_documents)}")
            logger.info(f"- Text files: {len(txt_documents)}")
            logger.info(f"- Markdown files: {len(md_documents)}")

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
            )
            texts = text_splitter.split_documents(documents)
            logger.info(f"Split into {len(texts)} text chunks.")

            logger.info("Creating vector store...")
            self.vector_store = FAISS.from_documents(texts, self.embeddings)

            # Save the vector store for future use
            self.save_vector_store()

        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}")
            raise

    def initialize_qa_chain(self) -> None:
        """Initialize the question-answering chain."""
        try:
            # Try loading a saved vector store first
            self.load_vector_store()

            if not self.vector_store:
                raise ValueError("Vector store not initialized. Please load documents first.")

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            )

            logger.info("QA chain initialized successfully.")

        except Exception as e:
            logger.error(f"Error initializing QA chain: {str(e)}")
            raise

    def get_answer(self, question: str) -> Dict[str, Any]:
        """
        Get answer for a given question.
        
        Args:
            question (str): User question
            
        Returns:
            Dict[str, Any]: Answer and relevant metadata
        """
        try:
            if not self.qa_chain:
                raise ValueError("QA chain not initialized.")

            result = self.qa_chain({"query": question})

            return {
                "answer": result.get("answer", "No answer found."),
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

    def save_vector_store(self) -> None:
        """Save the vector store for future use."""
        try:
            if self.vector_store:
                self.vector_store.save_local(self.vector_store_path)
                logger.info(f"Vector store saved to {self.vector_store_path}")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")
            raise

    def load_vector_store(self) -> None:
        """Load a previously saved vector store."""
        try:
            if os.path.exists(self.vector_store_path):
                self.vector_store = FAISS.load_local(
                    self.vector_store_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info(f"Vector store loaded from {self.vector_store_path}")
            else:
                logger.warning(f"No vector store found at {self.vector_store_path}.")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise
