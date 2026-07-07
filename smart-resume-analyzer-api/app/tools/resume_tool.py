from app.chains.resume_chain import chain

def analyze_resume(text: str):

    response = chain.invoke({
        "cv": text
    })

    return response.content