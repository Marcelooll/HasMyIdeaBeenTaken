from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.user import Owner
from app.models.project_context import ProjectContext
from app.repositories.base import BaseRepository


class RepositoryRepository(BaseRepository[Repository]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Repository)

    def get_by_name(self, repository_name: str) -> Repository | None:
        return self.session.query(Repository).filter(Repository.repository_name == repository_name).first()

    def create_with_context(self, *, owner_username: str, owner_profile_url: str | None, repository_name: str, source_platform: str, repository_url: str, raw_description: str | None, ai_generated_summary: str | None, embedding_vector: str | None) -> Repository:
        owner = self.session.query(Owner).filter(Owner.platform_username == owner_username).first()
        if owner is None:
            owner = Owner(platform_username=owner_username, platform_profile_url=owner_profile_url)
            self.session.add(owner)
            self.session.flush()

        repository = self.session.query(Repository).filter(Repository.repository_url == repository_url).first()
        if repository is None:
            repository = Repository(
                owner_id=owner.id,
                repository_name=repository_name,
                source_platform=source_platform,
                repository_url=repository_url,
            )
            self.session.add(repository)
            self.session.flush()

        context = self.session.query(ProjectContext).filter(ProjectContext.repository_id == repository.id).first()
        if context is None:
            context = ProjectContext(
                repository_id=repository.id,
                raw_description=raw_description,
                ai_generated_summary=ai_generated_summary,
                embedding_vector=embedding_vector,
            )
            self.session.add(context)
        else:
            context.raw_description = raw_description
            context.ai_generated_summary = ai_generated_summary
            context.embedding_vector = embedding_vector

        self.session.commit()
        self.session.refresh(repository)
        return repository
