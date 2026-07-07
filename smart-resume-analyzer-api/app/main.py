from fastapi import FastAPI

from app.routes.analyzer_routes import router as analyzer_router

from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Resume Analyzer API",
    version="1.0.0"
)

app.include_router(analyzer_router, prefix="/api")