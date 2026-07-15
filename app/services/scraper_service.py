from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.repositories.repository_repository import RepositoryRepository


@dataclass(slots=True)
class RepositorySeed:
    owner_username: str
    owner_profile_url: str | None
    repository_name: str
    source_platform: str = "github"
    repository_url: str = ""
    raw_description: str | None = None
    ai_generated_summary: str | None = None
    embedding_vector: str | None = None


class ScraperService:
    def __init__(self, repository: RepositoryRepository) -> None:
        self.repository = repository

    def ingest(self, seed: RepositorySeed) -> dict[str, Any]:
        created = self.repository.create_with_context(
            owner_username=seed.owner_username,
            owner_profile_url=seed.owner_profile_url,
            repository_name=seed.repository_name,
            source_platform=seed.source_platform,
            repository_url=seed.repository_url,
            raw_description=seed.raw_description,
            ai_generated_summary=seed.ai_generated_summary,
            embedding_vector=seed.embedding_vector,
        )
        return {
            "id": created.id,
            "repository_name": created.repository_name,
            "owner_username": seed.owner_username,
        }
