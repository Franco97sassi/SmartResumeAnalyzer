import os
import shutil

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from app.services.analyzer_service import analyze_text
from app.services.rag_service import index_pdf, ask
from app.agents.rag_agent import run_agent
from app.config.settings import settings
from app.repositories.history_repository import HistoryRepository

router = APIRouter()

repository = HistoryRepository()


class AnalyzeRequest(BaseModel):
    text: str


class Question(BaseModel):
    question: str


@router.post("/analyze")
def analyze(request: AnalyzeRequest):

    result = analyze_text(request.text)

    return result


@router.post("/upload")
def upload_pdf(file: UploadFile = File(...)):

    os.makedirs(settings.DOCUMENTS_PATH, exist_ok=True)

    path = os.path.join(
        settings.DOCUMENTS_PATH,
        file.filename
    )

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return index_pdf(path)


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


@router.get("/history")
def history():

    data = repository.get_all()

    return [
        {
            "id": item.id,
            "question": item.question,
            "answer": item.answer
        }
        for item in data
    ]

@router.get("/health")
def health():

    return {
        "status": "healthy",
        "application": "Smart Resume Analyzer",
        "version": "1.0.0"
    }