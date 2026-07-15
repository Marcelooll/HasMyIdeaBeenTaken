from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("owners.id"), nullable=False, index=True)
    repository_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    source_platform: Mapped[str] = mapped_column(String(64), nullable=False, default="github", index=True)
    repository_url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

    owner: Mapped["Owner"] = relationship(back_populates="repositories")
    project_context: Mapped["ProjectContext"] = relationship(back_populates="repository")

    def __repr__(self) -> str:
        return f"Repository(id={self.id}, name={self.repository_name!r})"
