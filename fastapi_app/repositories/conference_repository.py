from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from uuid import UUID
from models import Conference as ConferenceModel


class ConferenceRepository:

    def get_all(self, db: Session, skip: int = 0, limit: int = 20):
        return (
            db.query(ConferenceModel)
            .options(joinedload(ConferenceModel.tracks))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, id: UUID):
        return (
            db.query(ConferenceModel)
            .options(joinedload(ConferenceModel.tracks))
            .filter(ConferenceModel.id == id)
            .first()
        )

    def search(self, db: Session, query: str, skip: int = 0, limit: int = 20):
        return (
            db.query(ConferenceModel)
            .filter(
                or_(
                    ConferenceModel.name.ilike(f'%{query}%'),
                    ConferenceModel.description.ilike(f'%{query}%')
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
