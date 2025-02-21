# RAG Chatbot (Python Fullstack template)

A production-ready RAG (Retrieval Augmented Generation) based question-answering system that allows employees to query company documents using natural language. The system uses local LLMs through Ollama for privacy and performance, MongoDB for document storage, and provides a chat interface for easy interaction.

## 🌟 Features

* Local LLM Integration: Uses Ollama for running models locally, ensuring data privacy
* Document Management: Upload and process PDF documents directly through the chat interface
* MongoDB Storage: Persistent storage of documents with GridFS
* Vector Search: Efficient document retrieval using FAISS
* Modern Chat Interface: Built with Chainlit for a smooth user experience
* Containerized Services: Easy deployment with Docker Compose
* Async Processing: Built with FastAPI for high performance

## 🔧 System Architecture
```
           Upload PDFs
User ─────────────────▶ Chainlit UI ──────▶ MongoDB
                           │                   │
                           │                   │
                    Query  │                   │ Retrieve
                           │                   │ Documents
                           ▼                   ▼
                       FastAPI ◄─────────── RAG Model ◄─────── Local Ollama
                       Backend                 │
                           │                   │
                           └───────────────────┘
                              Return Answer
```

## 🚀 Getting Started
### Prerequisites

* Docker and Docker Compose
* Ollama (for local model running)
* Python 3.10+
* MongoDB (handled by Docker)

### Set-up

* Install Ollama locally (for Mac): 
```
brew install ollama
brew services start ollama
```

* Download required models: 
```
ollama run mistral
ollama run nomic-embed-text
```

* Clone the repository:
```
git clone https://github.com/yourusername/company-kb-assistant.git
cd company-kb-assistant
```

* Start the services:
```
docker-compose up --build
```

### Usage

* Access the chat interface at http://localhost:8501
* Upload company documents using the file upload button
* Start asking questions about your documents!

## 🏗️ Project Structure
```
rag-chatbot-python-fullstack-template/
├── backend/
│   ├── __init__.py
│   ├── model.py          # RAG model implementation
│   └── api.py            # FastAPI backend
├── frontend/
│   ├── __init__.py
│   └── app.py            # Chainlit chat interface
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── tests/
│   ├── __init__.py
│   ├── test_model.py
│   └── test_api.py
├── .env.example          # Example environment variables
├── .gitignore
├── docker-compose.yml    # Service orchestration
├── requirements.txt      # Python dependencies
├── chainlit.md          # Chainlit configuration
└── README.md
```

## 🔒 Security

All processing is done locally through Ollama
Documents are stored securely in MongoDB
No data leaves your infrastructure
Authentication can be added as needed

## 🛠️ Configuration
Environment variables (.env):
* CopyMONGODB_URL=mongodb://admin:password@mongodb:27017
* OLLAMA_URL=http://localhost:11434
* CHAINLIT_AUTH_SECRET=your-secret-key


## 🤝 Contributing

* Fork the repository
* Create your feature branch (git checkout -b feature/amazing-feature)
* Commit your changes (git commit -m 'Add amazing feature')
* Push to the branch (git push origin feature/amazing-feature)
* Open a Pull Request

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.


## 🙏 Acknowledgments

* Ollama for local LLM support
* LangChain for RAG implementation
* Chainlit for the chat interface
* FastAPI for the backend framework
* MongoDB for document storage