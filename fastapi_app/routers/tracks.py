from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Track as TrackModel
from schemas.session import TrackSchema

router = APIRouter(prefix="/api/v1/tracks", tags=["tracks"])

@router.get("/", response_model=list[TrackSchema])
def list_tracks(db: Session = Depends(get_db)):
    return db.query(TrackModel).options(
        joinedload(TrackModel.conference)
    ).all()
