from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    default_api_key: str = os.getenv("DEFAULT_API_KEY", "")
    default_api_base_url: str = os.getenv("DEFAULT_API_BASE_URL", "https://api.openai.com")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", 300))

settings = Settings()
