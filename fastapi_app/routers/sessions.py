from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from database import get_db
from services.session_service import SessionService
from repositories.session_repository import SessionRepository
from schemas.session import SessionSchema, SessionListSchema
from cache.redis_cache import cache_get, cache_set
from models import Registration as RegistrationModel

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


def get_service():
    return SessionService(SessionRepository())


@router.get("/")
def list_sessions(
    q: str = Query(None),
    track: str = Query(None),
    day: str = Query(None),
    tz: str = Query("UTC"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db)
):
    cache_key = f"sessions:list:{q}:{track}:{day}:{tz}:{page}:{page_size}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    service = get_service()
    skip = (page - 1) * page_size
    sessions, total = service.get_all_filtered(db, q=q, track=track, day=day, skip=skip, limit=page_size)

    results = []
    for s in sessions:
        registered = db.query(func.count(RegistrationModel.id)).filter(
            RegistrationModel.session_id == s.id
        ).scalar()
        item = SessionListSchema.model_validate(s)
        item_dict = item.model_dump()
        item_dict['registered'] = registered
        results.append(item_dict)

    response = {
        "count": total,
        "page": page,
        "results": results
    }
    cache_set(cache_key, response)
    return response


@router.get("/search/", response_model=list[SessionListSchema])
def search_sessions(
    query: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = get_service()
    return service.search(db, query, skip, limit)


@router.get("/{id}", response_model=SessionSchema)
def get_session(id: UUID, db: Session = Depends(get_db)):
    cache_key = f"sessions:detail:{id}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    service = get_service()
    session = service.get_by_id(db, id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    registered = db.query(func.count(RegistrationModel.id)).filter(
        RegistrationModel.session_id == session.id
    ).scalar()

    result = SessionSchema.model_validate(session)
    result_dict = result.model_dump()
    result_dict['registered'] = registered
    cache_set(cache_key, result_dict)
    return result_dict


@router.get("/{id}/availability/")
def get_availability(id: UUID, db: Session = Depends(get_db)):
    service = get_service()
    availability = service.get_availability(db, id)
    if not availability:
        raise HTTPException(status_code=404, detail="Session not found")
    return availability
