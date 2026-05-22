from pydantic import BaseModel,Field
from uuid import UUID
from datetime import datetime

class ConferenceSchema(BaseModel):
    id: UUID
    name: str
    description: str
    starts_at: datetime
    ends_at: datetime
    created: datetime
    modified: datetime

    class Config:
        from_attributes = True

class TrackSchema(BaseModel):
    id: UUID
    name: str
    conference: ConferenceSchema
    created: datetime
    modified: datetime
    color: str

    class Config:
        from_attributes = True

class SpeakersSchema(BaseModel):
    id: UUID
    name: str
    bio: str
    created: datetime
    modified: datetime
    affiliation: str

    class Config:
        from_attributes = True
class SessionListSchema(BaseModel):
    id: UUID
    title: str
    starts_at: datetime 
    ends_at: datetime | None = None
    capacity: int
    registered: int = 0

    class Config:
        from_attributes = True

class SessionSchema(BaseModel):
    id: UUID
    title: str
    abstract: str = Field(alias='description')
    starts_at: datetime
    capacity: int
    track: TrackSchema
    speakers: list[SpeakersSchema] = []
    created: datetime
    modified: datetime
    ends_at: datetime | None = None
    registered: int = 0

    class Config:
        from_attributes = True
        populate_by_name = True

class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Registration(BaseModel):
    id: UUID
    user: UserSchema
    session: SessionSchema
    registered_at: datetime
    created: datetime
    modified: datetime

    class Config:
        from_attributes = True

