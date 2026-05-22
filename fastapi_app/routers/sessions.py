from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from datetime import datetime, timezone
from database import get_db
from services.session_service import SessionService
from repositories.session_repository import SessionRepository
from schemas.session import SessionSchema, SessionListSchema
from cache.redis_cache import cache_get, cache_set
from models import Registration as RegistrationModel
import pytz

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


def get_service():
    return SessionService(SessionRepository())


def _parse_dt(v) -> datetime:
    if isinstance(v, datetime):
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)
    dt = datetime.fromisoformat(str(v))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _compute_relative_time(starts_at, ends_at, now: datetime) -> str:
    s = _parse_dt(starts_at)
    e = _parse_dt(ends_at) if ends_at else None
    if e and now >= e:
        return "ended"
    if now >= s:
        return "in_progress"
    minutes = int((s - now).total_seconds() / 60)
    return f"{minutes}m"

def inject_time(results: list[dict], now: datetime) -> None:
    for item in results:
        item["relative_time"] = _compute_relative_time(item["starts_at"], item.get("ends_at"), now)


def build_results(sessions, db) -> list[dict]:
    results = []
    for s in sessions:
        registered = db.query(func.count(RegistrationModel.id)).filter(
            RegistrationModel.session_id == s.id
        ).scalar()
        item = SessionListSchema.model_validate(s)
        item_dict = item.model_dump()
        item_dict["registered"] = registered
        results.append(item_dict)
    return results


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
 
@router.get("/today/")
def list_today_sessions(
    tz: str = Query("UTC"),
    q: str = Query(None),
    track: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        client_tz = pytz.timezone(tz)
    except pytz.exceptions.UnknownTimeZoneError:
        client_tz = pytz.utc

    today = datetime.now(client_tz).strftime("%Y-%m-%d")
    cache_key = f"sessions:today:{today}:{tz}:{q}:{track}:{page}:{page_size}"
    now = datetime.now(timezone.utc)

    cached = cache_get(cache_key)
    if cached:
        inject_time(cached["results"], now)
        return cached

    service = get_service()
    skip = (page - 1) * page_size
    sessions, total = service.get_all_filtered(db, q=q, track=track, day=today, tz=tz, skip=skip, limit=page_size)

    results = build_results(sessions, db)
    response = {"count": total, "page": page, "results": results}
    cache_set(cache_key, response, ttl=60)
    inject_time(response["results"], now)
    return response


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
    result_dict["registered"] = registered
    cache_set(cache_key, result_dict)
    return result_dict


@router.get("/{id}/availability/")
def get_availability(id: UUID, db: Session = Depends(get_db)):
    service = get_service()
    availability = service.get_availability(db, id)
    if not availability:
        raise HTTPException(status_code=404, detail="Session not found")
    return availability
