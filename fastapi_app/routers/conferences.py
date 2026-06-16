from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from services.conference_service import ConferenceService
from repositories.conference_repository import ConferenceRepository
from schemas.session import ConferenceSchema
from cache.redis_cache import cache_get, cache_set

router = APIRouter(prefix="/api/v1/conferences", tags=["conferences"])


def get_service():
    return ConferenceService(ConferenceRepository())


@router.get("/", response_model=list[ConferenceSchema])
def list_conferences(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    cache_key = f"conferences:list:{skip}:{limit}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    service = get_service()
    conferences = service.get_all(db, skip, limit)
    result = [ConferenceSchema.model_validate(c) for c in conferences]
    cache_set(cache_key, [r.model_dump() for r in result])
    return result


@router.get("/search/", response_model=list[ConferenceSchema])
def search_conferences(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    service = get_service()
    return service.search(db, query)


@router.get("/{id}", response_model=ConferenceSchema)
def get_conference(id: UUID, db: Session = Depends(get_db)):
    cache_key = f"conferences:detail:{id}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    service = get_service()
    conference = service.get_by_id(db, id)
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")

    result = ConferenceSchema.model_validate(conference)
    cache_set(cache_key, result.model_dump())
    return result
