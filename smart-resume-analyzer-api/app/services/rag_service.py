from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

from app.config.settings import settings
from app.rag.document_loader import load_pdf
from app.rag.text_splitter import split_documents
from app.rag.vector_store import create_vector_store
from app.repositories.history_repository import HistoryRepository
from app.utils.logger import logger
from app.utils.exceptions import ApplicationException

llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    keep_alive=settings.OLLAMA_KEEP_ALIVE,
    num_ctx=settings.OLLAMA_NUM_CTX,
    num_predict=settings.OLLAMA_NUM_PREDICT,
    temperature=settings.OLLAMA_TEMPERATURE
)

embeddings = OllamaEmbeddings(
model=settings.EMBEDDING_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    keep_alive=settings.OLLAMA_EMBEDDING_KEEP_ALIVE
) 

repository = HistoryRepository()


def ask(question: str):

    try:

        logger.info(f"Nueva pregunta: {question}")

        db = Chroma(
            persist_directory=settings.CHROMA_DB,
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

        repository.save(
            question=question,
            answer=response.content
        )

        logger.info("Historial guardado")

        return response.content

    except Exception as e:

        logger.exception(e)

        raise ApplicationException(
            "No fue posible procesar la consulta."
        )

def index_pdf(path: str):

    logger.info(f"Indexando PDF: {path}")

    docs = load_pdf(path)

    chunks = split_documents(docs)

    create_vector_store(chunks)

    logger.info(f"PDF indexado correctamente. Chunks: {len(chunks)}")

    return {
        "message": "Documento indexado correctamente",
        "chunks": len(chunks)
    }