from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parents[2]
DB_URL = "sqlite:///./app.db"


class Settings(BaseModel):
    app_name: str = "HasMyIdeaBeenTaken"
    debug: bool = Field(default=False)
    database_url: str = DB_URL
    max_search_results: int = 10


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
