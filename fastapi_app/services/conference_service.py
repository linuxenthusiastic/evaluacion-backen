from sqlalchemy.orm import Session
from uuid import UUID
from repositories.conference_repository import ConferenceRepository


class ConferenceService:
    def __init__(self, repository: ConferenceRepository):
        self.repository = repository

    def get_all(self, db: Session , skip: int = 0 , limit: int = 20):
        return self.repository.get_all(db,skip,limit)

    def get_by_id(self, db: Session, id: UUID):
        conference = self.repository.get_by_id(db,id)
        if not conference:
            return None
        return conference

    def search(self,db: Session, query: str,skip: int=0,limit: int = 20):
        return self.repository.search(db,query,skip,limit)

