from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from uuid import UUID
from models import Session as SessionModel

class SessionRepository:

    def get_all(self, db: Session, skip: int = 0, limit: int = 20):
        return (
            db.query(SessionModel)
            .options(
                joinedload(SessionModel.track)
                .joinedload(SessionModel.track.property.mapper.class_.conference),
                joinedload(SessionModel.speakers)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, id: UUID):
        return (
            db.query(SessionModel)
            .options(
                joinedload(SessionModel.track),
                joinedload(SessionModel.speakers)
            )
            .filter(SessionModel.id == id)
            .first()
        )

    def search(self, db: Session, query: str, skip: int = 0, limit: int = 20):
        return (
            db.query(SessionModel)
            .filter(
                or_(
                    SessionModel.title.ilike(f'%{query}%'),
                    SessionModel.description.ilike(f'%{query}%')
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
