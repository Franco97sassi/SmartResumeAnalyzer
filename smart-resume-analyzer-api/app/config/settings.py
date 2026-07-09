import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    OLLAMA_KEEP_ALIVE = os.getenv(
        "OLLAMA_KEEP_ALIVE",
        "10m"
    )

    OLLAMA_EMBEDDING_KEEP_ALIVE = int(os.getenv(
        "OLLAMA_EMBEDDING_KEEP_ALIVE",
        "600"
    ))

    OLLAMA_NUM_CTX = int(os.getenv(
        "OLLAMA_NUM_CTX",
        "2048"
    ))

    OLLAMA_NUM_PREDICT = int(os.getenv(
        "OLLAMA_NUM_PREDICT",
        "512"
    ))

    OLLAMA_TEMPERATURE = float(os.getenv(
        "OLLAMA_TEMPERATURE",
        "0.2"
    ))
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