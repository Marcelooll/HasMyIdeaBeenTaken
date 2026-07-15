from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes.health import router as health_router
from app.api.routes.search import router as search_router
from app.db.session import init_db

app = FastAPI(title="HasMyIdeaBeenTaken", version="0.1.0")

init_db()

app.include_router(health_router)
app.include_router(search_router, prefix="/api")

BASE_DIR = Path(__file__).resolve().parents[1]


@app.get("/")
def root() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "index.html")
