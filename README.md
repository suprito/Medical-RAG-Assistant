## Medical RAG Assistant:
A full-stack Generative AI application that uses Retrieval-Augmented Generation (RAG) to provide accurate medical information based on a specific textbook knowledge base. The system features a FastAPI backend and a Streamlit frontend, deployed as a containerized application.

## Tech Stack:
LLM: IBM Granite-3.0-1b-instruct
Framework: LangChain
Vector Database: ChromaDB
Embeddings: HuggingFace Embeddings (msmarco-MiniLM-L6-v3)
Backend: FastAPI
Frontend: Streamlit
Deployment: Docker & Hugging Face Spaces

## Live Demo:
The application is deployed on Hugging Face Spaces: https://huggingface.co/spaces/Suprito/Medical-RAG-Assistant
Note: If the space is in sleep mode, click wake to start the application.

## Azure Deployment & Architecture
This application is containerized and deployed as an Enterprise RAG solution on **Azure**.

### **Infrastructure Components**
* **Container Registry (ACR):** Used for private hosting and versioning of the Docker image.
* **App Service (Web App for Containers):** Handles the orchestration of the Streamlit/FastAPI stack.
* **Resource Optimization:** Configured `WEBSITES_CONTAINER_START_TIME_LIMIT = 1800` to allow sufficient time for the **IBM Granite 3.0** model weights and the 600-page medical index to load into memory.

### **Local Setup vs. Cloud**
While local development utilized a simple Python environment, the production version leverages **Docker** to ensure consistency across the **Central India** Azure region.
