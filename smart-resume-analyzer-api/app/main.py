from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analyzer_routes import router as analyzer_router
from app.database import Base, engine
from app.utils.exceptions import (
    ApplicationException,
    application_exception_handler,
    generic_exception_handler
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Resume Analyzer API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyzer_router, prefix="/api")

app.add_exception_handler(
    ApplicationException,
    application_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)