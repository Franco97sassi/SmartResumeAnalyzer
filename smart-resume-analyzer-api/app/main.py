from fastapi import FastAPI

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

app.include_router(analyzer_router, prefix="/api")

app.add_exception_handler(
    ApplicationException,
    application_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)