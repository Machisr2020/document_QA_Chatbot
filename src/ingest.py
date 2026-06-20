import os
import chromadb

from docx import Document
from sentence_transformers import SentenceTransformer

DATA_FOLDER = "data"
DB_PATH = "db"

model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_docx(file_path):
    doc = Document(file_path)

    text = "\n".join(
        p.text for p in doc.paragraphs
        if p.text.strip()
    )

    return text


def load_documents():
    docs = []

    for file_name in os.listdir(DATA_FOLDER):

        if file_name.endswith(".docx"):

            path = os.path.join(DATA_FOLDER, file_name)

            docs.append(extract_docx(path))

    return docs


def chunk_text(text, chunk_size=500, overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def main():

    docs = load_documents()

    all_chunks = []

    for doc in docs:

        all_chunks.extend(chunk_text(doc))

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name="documents"
    )

    for i, chunk in enumerate(all_chunks):

        embedding = model.encode(chunk).tolist()

        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk],
            embeddings=[embedding]
        )

    print("Chunks Indexed:", len(all_chunks))


if __name__ == "__main__":
    main()