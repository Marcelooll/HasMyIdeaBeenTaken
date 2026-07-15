from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    platform_username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    platform_profile_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    repositories: Mapped[list["Repository"]] = relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f"Owner(id={self.id}, username={self.platform_username!r})"
