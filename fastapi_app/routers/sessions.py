from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from services.session_service import SessionService
from repositories.session_repository import SessionRepository
from schemas.session import SessionSchema, SessionListSchema
from cache.redis_cache import cache_get, cache_set

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


def get_service():
    return SessionService(SessionRepository())


@router.get("/", response_model=list[SessionListSchema])
def list_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    cache_key = f"sessions:list:{skip}:{limit}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    service = get_service()
    sessions = service.get_all(db, skip, limit)
    result = [SessionListSchema.model_validate(s) for s in sessions]
    cache_set(cache_key, [r.model_dump() for r in result])
    return result


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

    result = SessionSchema.model_validate(session)
    cache_set(cache_key, result.model_dump())
    return result


@router.get("/{id}/availability/")
def get_availability(id: UUID, db: Session = Depends(get_db)):
    service = get_service()
    availability = service.get_availability(db, id)
    if not availability:
        raise HTTPException(status_code=404, detail="Session not found")
    return availability
