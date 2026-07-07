from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2"
)

def general_chat(question: str):

    response = llm.invoke(question)

    return response.content