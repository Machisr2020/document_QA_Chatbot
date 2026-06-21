# Document Question Answer Chatbot

## Project Overview

This project is an AI-powered Document Question Answering Chatbot that allows users to ask questions based on the contents of uploaded documents.

The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from indexed documents and generate accurate answers using Google's Gemini model.

## Features

* Document-based Question Answering
* DOCX Document Processing
* Text Chunking
* Semantic Search using Embeddings
* ChromaDB Vector Database
* Gemini AI Response Generation
* Streamlit User Interface
* Live Web Deployment

## Tech Stack

* Python
* Streamlit
* ChromaDB
* Sentence Transformers
* Google Gemini API
* Python Docx
* GitHub

## Project Architecture

1. Documents are loaded from the data folder.
2. Documents are split into smaller chunks.
3. Chunks are converted into embeddings.
4. Embeddings are stored in ChromaDB.
5. User enters a question.
6. Similar chunks are retrieved from ChromaDB.
7. Gemini generates an answer based on retrieved context.
8. Answer is displayed in Streamlit.

## Installation

Clone the repository:

git clone <repository-url>

Install dependencies:

pip install -r requirements.txt

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY

Run indexing:

python src/ingest.py

Run application:

streamlit run src/main.py

## Deployment

The application is deployed using Streamlit Community Cloud.

Live Demo Link:
https://documentappchatbot-inhpl4idgruky4wm6wqhrp.streamlit.app/

## Future Enhancements
* PDF Support
* Multiple Document Upload
* Chat History
* Source Citation Display
* Advanced Search Ranking

## Author

Maha
