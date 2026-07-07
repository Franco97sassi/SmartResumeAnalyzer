import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "nomic-embed-text"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///history.db"
    )

    CHROMA_DB = os.getenv(
        "CHROMA_DB",
        "./db"
    )

    DOCUMENTS_PATH = os.getenv(
        "DOCUMENTS_PATH",
        "./documents"
    )


settings = Settings()