from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="llama3.2",
    temperature=0.2
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