from app.rag.document_loader import load_pdf
from app.rag.text_splitter import split_documents
from app.rag.vector_store import create_vector_store

from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

from app.database import SessionLocal
from app.models.query_history import QueryHistory

llm = ChatOllama(model="llama3.2")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


def ask(question: str):

    db = Chroma(
        persist_directory="./db",
        embedding_function=embeddings
    )

    docs = db.similarity_search(question, k=4)

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
Responde utilizando únicamente el siguiente contexto.

Contexto:

{context}

Pregunta:

{question}
"""

    response = llm.invoke(prompt)

    # Guardar historial en SQLite
    session = SessionLocal()

    history = QueryHistory(
        question=question,
        answer=response.content
    )

    session.add(history)
    session.commit()
    session.close()

    return response.content


def index_pdf(path: str):

    docs = load_pdf(path)

    chunks = split_documents(docs)

    create_vector_store(chunks)

    return {
        "message": "Documento indexado correctamente",
        "chunks": len(chunks)
    }