from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_BASE: str
    AZURE_OPENAI_ACCESS_KEY: str
    AZURE_OPENAI_API_VERSION: str = "2024-05-01-preview"
    AZURE_OPENAI_MODEL_ID: str = "gpt-4o-mini"

    # Unstructured.io Configuration
    UNSTRUCTURED_API_KEY: str
    UNSTRUCTURED_BASE_URL: str

    # PostgreSQL Configuration
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings() 