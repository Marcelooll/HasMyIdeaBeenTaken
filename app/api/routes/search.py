from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import session_factory
from app.schemas.repository import SearchRequest
from app.services.search_service import SearchService

router = APIRouter()


def get_db() -> Session:
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


@router.post("/search")
def search_repositories(payload: SearchRequest, db: Session = Depends(get_db)) -> dict[str, object]:
    service = SearchService(db)
    matches = service.search(payload.query, limit=10)
    if not matches:
        raise HTTPException(status_code=404, detail="No matching repositories found")
    return {
        "query": payload.query,
        "matches": [
            {
                "repository_name": match.repository_name,
                "owner_username": match.owner_username,
                "score": match.score,
                "summary": match.summary,
                "url": match.url,
            }
            for match in matches
        ],
    }
