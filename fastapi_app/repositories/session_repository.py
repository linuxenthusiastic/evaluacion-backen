from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from uuid import UUID
from models import Session as SessionModel, Registration as RegistrationModel
from datetime import datetime
import pytz


class SessionRepository:

    def get_all_filtered(self, db: Session, q=None, track=None, day=None, skip=0, limit=12):
        query = db.query(SessionModel).options(
            joinedload(SessionModel.track).joinedload(SessionModel.track.property.mapper.class_.conference),
            joinedload(SessionModel.speakers)
        )

        if q:
            query = query.filter(
                or_(
                    SessionModel.title.ilike(f'%{q}%'),
                    SessionModel.description.ilike(f'%{q}%')
                )
            )

        if track:
            query = query.join(SessionModel.track).filter(
                SessionModel.track.property.mapper.class_.id == track
            )

        if day:
            try:
                day_dt = datetime.strptime(day, '%Y-%m-%d')
                query = query.filter(
                    func.date(SessionModel.starts_at) == day_dt.date()
                )
            except ValueError:
                pass

        total = query.count()
        sessions = query.offset(skip).limit(limit).all()
        return sessions, total

    def get_by_id(self, db: Session, id: UUID):
        return (
            db.query(SessionModel)
            .options(
                joinedload(SessionModel.track).joinedload(
                    SessionModel.track.property.mapper.class_.conference
                ),
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
