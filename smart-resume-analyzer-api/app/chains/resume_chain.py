from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.config.settings import settings
llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    keep_alive=settings.OLLAMA_KEEP_ALIVE,
    num_ctx=settings.OLLAMA_NUM_CTX,
    num_predict=settings.OLLAMA_NUM_PREDICT,
    temperature=settings.OLLAMA_TEMPERATURE
)

prompt = ChatPromptTemplate.from_template("""
Eres un Senior Software Architect especializado en selección de personal.

Analiza el siguiente CV.

Devuelve:

1. Resumen
2. Seniority
3. Tecnologías detectadas
4. Fortalezas
5. Debilidades
6. Recomendaciones

CV:

{cv}
""")

chain = prompt | llm