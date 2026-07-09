from langchain_ollama import ChatOllama
from app.config.settings import settings
llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    keep_alive=settings.OLLAMA_KEEP_ALIVE,
    num_ctx=settings.OLLAMA_NUM_CTX,
    num_predict=settings.OLLAMA_NUM_PREDICT,
    temperature=settings.OLLAMA_TEMPERATURE
)


def general_chat(question: str):

    response = llm.invoke(question)

    return response.content