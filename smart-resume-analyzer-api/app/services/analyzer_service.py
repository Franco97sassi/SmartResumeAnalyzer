# import ollama

# def analyze_text(text: str):

#     prompt = f"""
# Analiza el siguiente CV o texto.

# Devuelve:

# - Resumen
# - Nivel técnico
# - Tecnologías detectadas
# - Fortalezas
# - Debilidades
# - Recomendaciones

# Texto:

# {text}
# """

#     response = ollama.chat(
#         model="llama3.2",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     return {
#         "analysis": response["message"]["content"]
#     }
from app.chains.resume_chain import chain

def analyze_text(text: str):

    response = chain.invoke(
        {
            "cv": text
        }
    )

    return {
        "analysis": response.content
    }