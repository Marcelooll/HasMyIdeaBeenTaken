from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def seed_demo_data() -> None:
    from app.models.project_context import ProjectContext
    from app.models.repository import Repository
    from app.models.user import Owner

    with session_factory() as session:
        demo_url = "https://github.com/octocat/hello-world"
        existing_repository = session.execute(
            select(Repository).where(Repository.repository_url == demo_url)
        ).scalar_one_or_none()

        if existing_repository is not None:
            return

        owner = session.execute(
            select(Owner).where(Owner.platform_username == "octocat")
        ).scalar_one_or_none()
        if owner is None:
            owner = Owner(
                platform_username="octocat",
                platform_profile_url="https://github.com/octocat",
            )
            session.add(owner)
            session.flush()

        repository = Repository(
            owner_id=owner.id,
            repository_name="hello-world",
            source_platform="github",
            repository_url=demo_url,
        )
        session.add(repository)
        session.flush()

        context = ProjectContext(
            repository_id=repository.id,
            raw_description="A simple hello world project for demo purposes.",
            ai_generated_summary="Beginner-friendly example repository that demonstrates foundational software development patterns.",
            embedding_vector="demo-embedding-vector",
        )
        session.add(context)
        session.commit()


def init_db() -> None:
    from app.models import repository, user, project_context  # noqa: F401

    Base.metadata.create_all(bind=engine)
    seed_demo_data()
