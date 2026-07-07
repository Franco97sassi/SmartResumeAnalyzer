from app.services.rag_service import ask

def search_documents(question: str):
    return ask(question)