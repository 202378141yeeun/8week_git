import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Settings:
    """기본 설정 모음"""

    PROJECT_NAME: str = "AI Chat Demo"
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


settings = Settings()
