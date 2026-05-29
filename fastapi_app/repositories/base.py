from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from uuid import UUID


class BaseRepository(ABC):


    @abstractmethod
    def get_by_id(self, db: Session, id: UUID):
        ...

    @abstractmethod
    def search(self, db: Session, query: str, skip: int, limit: int):
        ...
