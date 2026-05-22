from fastapi import FastAPI
from routers import sessions, conferences, tracks

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
def health():
    return {"status": "ok"}
