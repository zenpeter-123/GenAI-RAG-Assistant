from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise GenAI Document Assistant"
    API_V1_STR: str = "/api/v1"
    
    # LLM és Embedding beállítások
    OPENAI_API_KEY: str
    DEFAULT_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Vektor adatbázis mentési helye
    CHROMA_PERSIST_DIR: str = "./chroma_db"

    class Config:
        env_file = ".env"
        extra = "ignore"

# Ezt az objektumot fogjuk importálni a projekt többi részén
settings = Settings()