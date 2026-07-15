from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.models.project_context import ProjectContext
from app.models.repository import Repository
from app.models.user import Owner


@dataclass(slots=True)
class SearchMatch:
    repository_name: str
    owner_username: str
    score: float
    summary: str | None
    url: str


class SearchService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def search(self, query: str, limit: int = 10) -> list[SearchMatch]:
        normalized_query = query.strip().lower()
        if not normalized_query:
            return []

        results = (
            self.session.query(Repository, Owner, ProjectContext)
            .join(Owner, Repository.owner_id == Owner.id)
            .join(ProjectContext, ProjectContext.repository_id == Repository.id)
            .filter(
                (Repository.repository_name.ilike(f"%{normalized_query}%"))
                | (Owner.platform_username.ilike(f"%{normalized_query}%"))
                | (ProjectContext.ai_generated_summary.ilike(f"%{normalized_query}%"))
            )
            .limit(limit)
            .all()
        )

        matches: list[SearchMatch] = []
        for repository, owner, context in results:
            score = 1.0 if normalized_query in repository.repository_name.lower() else 0.5
            matches.append(
                SearchMatch(
                    repository_name=repository.repository_name,
                    owner_username=owner.platform_username,
                    score=score,
                    summary=context.ai_generated_summary,
                    url=repository.repository_url,
                )
            )

        return matches
