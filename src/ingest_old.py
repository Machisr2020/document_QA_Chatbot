import os
from pypdf import PdfReader
from docx import Document
from dotenv import load_dotenv

import chromadb
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DATA_FOLDER = "data"
DB_PATH = "db"
COLLECTION_NAME = "document_knowledge_base"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def extract_pdf(file_path):
    pages = []

    reader = PdfReader(file_path)

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            pages.append(
                {
                    "text": text,
                    "metadata": {
                        "source": os.path.basename(file_path),
                        "page": page_num
                    }
                }
            )

    return pages


def extract_docx(file_path):
    doc = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    )

    return [
        {
            "text": text,
            "metadata": {
                "source": os.path.basename(file_path),
                "page": 1
            }
        }
    ]


def load_documents():
    documents = []

    for file_name in os.listdir(DATA_FOLDER):

        file_path = os.path.join(DATA_FOLDER, file_name)

        if file_name.lower().endswith(".pdf"):
            documents.extend(extract_pdf(file_path))

        elif file_name.lower().endswith(".docx"):
            documents.extend(extract_docx(file_path))

    return documents


def chunk_documents(documents):
    chunks = []

    for doc in documents:

        text = doc["text"]
        metadata = doc["metadata"]

        start = 0

        while start < len(text):

            end = min(start + CHUNK_SIZE, len(text))

            chunk_text = text[start:end]

            chunks.append(
                {
                    "text": chunk_text,
                    "metadata": metadata
                }
            )

            start += (CHUNK_SIZE - CHUNK_OVERLAP)

    return chunks


def save_to_chroma(chunks):

    client = chromadb.PersistentClient(path=DB_PATH)

    embedding_function = GoogleGenerativeAiEmbeddingFunction(
        api_key=GEMINI_API_KEY,
        model_name="models/text-embedding-004"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        ids.append(f"chunk_{i}")

        documents.append(chunk["text"])

        metadatas.append(chunk["metadata"])

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Indexed {len(chunks)} chunks successfully.")


def main():

    print("Loading documents...")

    docs = load_documents()

    print(f"Documents loaded: {len(docs)}")

    chunks = chunk_documents(docs)

    print(f"Chunks created: {len(chunks)}")

    save_to_chroma(chunks)

    print("Done.")


if __name__ == "__main__":
    main()