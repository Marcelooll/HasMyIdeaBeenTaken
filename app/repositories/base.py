from collections.abc import Iterable
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    def __init__(self, session: Session, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    def add(self, obj: ModelT) -> ModelT:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def add_many(self, objs: Iterable[ModelT]) -> None:
        self.session.add_all(list(objs))
        self.session.commit()

    def get_by_id(self, obj_id: Any) -> ModelT | None:
        return self.session.get(self.model, obj_id)

    def list(self) -> list[ModelT]:
        return list(self.session.scalars(select(self.model)).all())

    def delete(self, obj: ModelT) -> None:
        self.session.delete(obj)
        self.session.commit()
