# RAG Chatbot (Python Fullstack template)

A RAG (Retrieval Augmented Generation) based question-answering prrof-of-concept (PoC) system that allows a user to query target documents using natural language. The system uses local LLMs through Ollama for privacy and performance and provides a chat interface for easy interaction. The entire codebase (both backend and frontend are developed using Python3.10).

## 🌟 Features

* Local LLM Integration: Uses Ollama for running models locally, ensuring data privacy
* Vector Search: Efficient document retrieval using FAISS
* Modern Chat Interface: Built with Chainlit for a smooth user experience
* Containerized Services: Easy deployment with Docker Compose
* Async Processing: Built with FastAPI for high performance

## 🔧 System Architecture
```
        
User ───────────────▶ Chainlit UI       Documents (txt/md/pdf)
                           │                     │
                           │                     │
                    Query  │                     │ Retrieve
                           │                     │ Documents
                           ▼                     ▼
                       FastAPI ◄───────────  RAG Model ◄─────── Local Ollama
                       Backend                   │
                           │                     │
                           └─────────────────────┘
                                Return Answer
```

## 🚀 Getting Started
### Prerequisites

* Docker and Docker Compose
* Ollama (for local model running)
* Python 3.10+


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
git clone https://github.com/yourusername/rag-chatbot-python-fullstack-template.git
cd rag-chatbot-python-fullstack-template
```

* Start the services:
```
docker-compose build
docker-compose up -d
```

### Usage

* Access the chat interface at http://localhost:8505
* Keep your files under the documents directory
* Start asking questions about your documents!

## 🏗️ Project Structure
```
rag-chatbot-python-fullstack-template/
├── backend/
│   ├── model.py          # RAG model implementation
│   └── api.py            # FastAPI backend
├── frontend/
│   └── app.py            # Chainlit chat interface
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── requirements/
│   ├── backend_requirements.txt
│   └── frontend_requirements.txt
├── documents/            # Put/organize your documents here
│   ├── test_file_1.txt 
│   └── test_file_2.md
├── .env.example          # Example environment variables
├── .gitignore
├── docker-compose.yml    # Service orchestration
├── requirements.txt      # Python dependencies as a whole (not needed)
├── chainlit.md          # Chainlit configuration
└── README.md
```

## 🔒 Security

All processing is done locally through Ollama
No data leaves your infrastructure
Authentication can be added as needed


## 🛠️ Configuration
Environment variables (.env):
* OLLAMA_URL=http://localhost:11434
* CHAINLIT_AUTH_SECRET=your-secret-key


## Kubernetes Deployment
Added sample kubernetes config files under `kubernetes-template` folder. 
You need to modify values before production usage.
Read the [Deployment Steps](kubernetes-template/README-kubernetes.md) guide for details.


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