from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
 
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)
def create_vector_store(documents):

    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./db"
    )

    return vectordb