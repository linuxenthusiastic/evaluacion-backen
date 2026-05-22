from pydantic import BaseModel
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

    class Config:
        from_attributes = True

class SpeakersSchema(BaseModel):
    id: UUID
    name: str
    bio: str
    created: datetime
    modified: datetime

    class Config:
        from_attributes = True
class SessionListSchema(BaseModel):
    id: UUID
    title: str
    starts_at: datetime
    capacity: int
    class Config:
        from_attributes = True

class SessionSchema(BaseModel):
    id: UUID
    title: str
    description: str
    starts_at: datetime
    capacity: int
    track: TrackSchema
    speakers: list[SpeakersSchema] = []
    created: datetime
    modified: datetime

    class Config:
        from_attributes = True

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

