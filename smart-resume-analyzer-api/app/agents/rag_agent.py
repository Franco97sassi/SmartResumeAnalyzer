from typing import TypedDict
from langgraph.graph import StateGraph, END
from app.tools.resume_tool import analyze_resume
from app.tools.rag_tool import search_documents
from app.tools.general_tool import general_chat
from app.services.rag_service import ask
from app.chains.resume_chain import chain


class AgentState(TypedDict):
    question: str
    route: str
    answer: str


def classify_question(state: AgentState):

    question = state["question"].lower()

    pdf_keywords = [
        "documento",
        "pdf",
        "texto",
        "archivo",
        "según el documento",
        "qué dice",
        "menciona",
        "contenido"
    ]

    resume_keywords = [
        "cv",
        "curriculum",
        "resume",
        "linkedin"
    ]

    if any(keyword in question for keyword in pdf_keywords):
        return {
            **state,
            "route": "rag"
        }

    if any(keyword in question for keyword in resume_keywords):
        return {
            **state,
            "route": "resume"
        }

    return {
        **state,
        "route": "llm"
    }

def answer_with_rag(state: AgentState):
    return {
        **state,
        "answer": search_documents(state["question"])
    }


def answer_with_llm(state: AgentState):
    return {
        **state,
        "answer": general_chat(state["question"])
    }
def answer_with_resume(state: AgentState):

    return {
        **state,
        "answer": analyze_resume(state["question"])
    }
def route_question(state: AgentState):

    if state["route"] == "rag":
        return "rag"

    if state["route"] == "resume":
        return "resume"

    return "llm"


graph = StateGraph(AgentState)

graph.add_node("classify", classify_question)
graph.add_node("rag", answer_with_rag)
graph.add_node("llm", answer_with_llm)
graph.add_node("resume", answer_with_resume)
graph.set_entry_point("classify")

graph.add_conditional_edges(
    "classify",
    route_question,
    {
        "rag": "rag",
        "llm": "llm",
        "resume": "resume"
    }
)
graph.add_edge("resume", END)
graph.add_edge("rag", END)
graph.add_edge("llm", END)

agent = graph.compile()


def run_agent(question: str):
    result = agent.invoke({
        "question": question,
        "route": "",
        "answer": ""
    })

    return result["answer"]