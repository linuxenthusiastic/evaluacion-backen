from sqlalchemy.orm import Session
from uuid import UUID
from repositories.session_repository import SessionRepository


class SessionService:

    def __init__(self, repository: SessionRepository):
        self.repository = repository

    def get_all(self, db: Session, skip: int = 0, limit: int = 20):
        return self.repository.get_all(db, skip, limit)

    def get_by_id(self, db: Session, id: UUID):
        session = self.repository.get_by_id(db, id)
        if not session:
            return None
        return session

    def search(self, db: Session, query: str, skip: int = 0, limit: int = 20):
        return self.repository.search(db, query, skip, limit)

    def get_availability(self, db: Session, id: UUID):
        session = self.repository.get_by_id(db, id)
        if not session:
            return None
        registered = len(session.registrations)
        available  = session.capacity - registered
        return {
            "session_id": id,
            "capacity":   session.capacity,
            "registered": registered,
            "available":  max(0, available),
            "is_full":    available <= 0
        }
