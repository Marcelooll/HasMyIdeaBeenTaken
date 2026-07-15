from pydantic import BaseModel, Field


class RepositoryCreate(BaseModel):
    owner_username: str = Field(..., min_length=1, max_length=255)
    owner_profile_url: str | None = Field(default=None, max_length=500)
    repository_name: str = Field(..., min_length=1, max_length=255)
    source_platform: str = Field(default="github", max_length=64)
    repository_url: str = Field(..., min_length=1, max_length=500)
    raw_description: str | None = Field(default=None)
    ai_generated_summary: str | None = Field(default=None)
    embedding_vector: str | None = Field(default=None, max_length=2048)


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
