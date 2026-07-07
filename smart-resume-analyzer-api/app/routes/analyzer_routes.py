from fastapi import APIRouter
from pydantic import BaseModel
from app.services.analyzer_service import analyze_text
from fastapi import UploadFile, File
import shutil
import os
from app.services.rag_service import ask
from app.services.rag_service import index_pdf
from app.agents.rag_agent import run_agent
router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: str

@router.post("/analyze")
def analyze(request: AnalyzeRequest):
    result = analyze_text(request.text)
    return result

@router.post("/upload")

def upload_pdf(file: UploadFile = File(...)):

    os.makedirs("documents", exist_ok=True)

    path = f"documents/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return index_pdf(path)

class Question(BaseModel):
    question: str


@router.post("/ask")

def ask_question(question: Question):

    return {
        "answer": ask(question.question)
    }


@router.post("/agent")
def agent_question(question: Question):
    return {
        "answer": run_agent(question.question)
    }