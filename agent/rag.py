import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from langchain_groq import ChatGroq
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

PROPERTY_FILES = {
    "grandview_hotel": "data/grandview_hotel.md",
    "golden_spoon": "data/golden_spoon.md",
    "azure_beach": "data/azure_beach.md",
}

# ChromaDB client
_client = chromadb.Client()
_embedding_fn = DefaultEmbeddingFunction()


def load_vector_store(property_key: str):
    file_path = PROPERTY_FILES[property_key]

    # 1. Load
    with open(file_path, "r") as f:
        text = f.read()

    # 2. Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_text(text)

    # 3. Embed + 4. Store
    collection = _client.get_or_create_collection(
        name=property_key,
        embedding_function=_embedding_fn,
    )

    collection.add(
        documents=chunks,
        ids=[f"{property_key}_{i}" for i in range(len(chunks))],
    )

    return collection


def build_qa_chain(property_key: str):
    collection = load_vector_store(property_key)

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
    )

    def answer(question: str) -> str:
        # 5. Retrieve
        results = collection.query(
            query_texts=[question],
            n_results=3,
        )
        context = "\n\n".join(results["documents"][0])

        # 6. Generate
        prompt = f"""You are a helpful hotel assistant.
Use the following information to answer the guest's question.
If you don't know, say so politely.

Context:
{context}

Question: {question}
Answer:"""

        response = llm.invoke(prompt)
        return response.content

    return answer
