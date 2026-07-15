from app.db.session import init_db, session_factory
from app.repositories.repository_repository import RepositoryRepository
from app.services.scraper_service import RepositorySeed, ScraperService


def main() -> None:
    init_db()
    session = session_factory()
    repo = RepositoryRepository(session)
    service = ScraperService(repo)

    service.ingest(
        RepositorySeed(
            owner_username="octocat",
            owner_profile_url="https://github.com/octocat",
            repository_name="hello-world",
            source_platform="github",
            repository_url="https://github.com/octocat/hello-world",
            raw_description="A simple hello world project for demonstration purposes.",
            ai_generated_summary="A beginner-friendly example repository that demonstrates foundational software development patterns.",
            embedding_vector="demo-embedding-vector",
        )
    )
    session.close()
    print("Demo repository ingested successfully.")


if __name__ == "__main__":
    main()
