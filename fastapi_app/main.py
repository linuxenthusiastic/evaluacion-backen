from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from routers import sessions, conferences, tracks
from database import get_db
from cache.redis_cache import get_redis

app = FastAPI(
    title="Conference API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(sessions.router)
app.include_router(conferences.router)
app.include_router(tracks.router)


@app.get("/api/v1/healthz")
def health(db: Session = Depends(get_db)):
    postgres_ok = False
    redis_ok = False

    try:
        db.execute(text("SELECT 1"))
        postgres_ok = True
    except Exception:
        postgres_ok = False

    try:
        client = get_redis()
        redis_ok = client is not None
    except Exception:
        redis_ok = False

    status_code = 200 if postgres_ok else 503

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ok" if postgres_ok else "error",
            "postgres": "ok" if postgres_ok else "down",
            "redis": "ok" if redis_ok else "degraded"
        }
    )
