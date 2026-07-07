from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from app.config.settings import settings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)
def create_vector_store(documents):

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
persist_directory=settings.CHROMA_DB    )

    return vectordb