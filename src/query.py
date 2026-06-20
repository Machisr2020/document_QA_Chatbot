import os
import chromadb

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from google import genai

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="db")

collection = client.get_collection("documents")

gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_question(question):

    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context = "\n".join(
        results["documents"][0]
    )

    prompt = f"""
Answer only from the provided context.

Context:
{context}

Question:
{question}
"""

    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    while True:

        question = input("\nQuestion: ")

        if question.lower() == "exit":
            break

        answer = ask_question(question)

        print("\nAnswer:")
        print(answer)