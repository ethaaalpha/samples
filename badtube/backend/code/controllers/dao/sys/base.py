from abc import ABC
from typing import Generic, TypeVar
from sqlmodel import SQLModel, Session, select

T = TypeVar("T", bound=SQLModel)

class DataService(Generic[T], ABC):
    model: type[T]

    def __init__(self, session: Session):
        self.session = session

    def upsert(self, obj: T):
        if type(obj) is not self.model:
            raise TypeError(f"Invalid type, use: {self.model} instead of {type(obj)}")

        self.session.add(obj)
        self.session.flush()
        self.session.refresh(obj)

    def delete(self, obj: T):
        if type(obj) is not self.model:
            raise TypeError(f"Invalid type, use: {self.model} instead of {type(obj)}")

        self.session.delete(obj)

    def all(self) -> list[T]:
        return self.session.exec(select(self.model)).all()

    def get(self, primary_key) -> T | None:
        return self.session.get(self.model, primary_key)
