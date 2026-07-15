from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ProjectContext(Base):
    __tablename__ = "project_context"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"), nullable=False, unique=True, index=True)
    raw_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_generated_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    embedding_vector: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    repository: Mapped["Repository"] = relationship(back_populates="project_context")

    def __repr__(self) -> str:
        return f"ProjectContext(id={self.id}, repository_id={self.repository_id})"
