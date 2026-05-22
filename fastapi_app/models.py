import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base


class Conference(Base):
    __tablename__ = 'conference'
    __table_args__ = {'schema': 'content'}

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name        = Column(String(255), nullable=False)
    description = Column(Text, default='')
    starts_at   = Column(DateTime(timezone=True), nullable=False)
    ends_at     = Column(DateTime(timezone=True), nullable=False)
    created     = Column(DateTime(timezone=True))
    modified    = Column(DateTime(timezone=True))

    tracks = relationship('Track', back_populates='conference')


class Track(Base):
    __tablename__ = 'track'
    __table_args__ = {'schema': 'content'}

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name          = Column(String(255), nullable=False)
    conference_id = Column(UUID(as_uuid=True), ForeignKey('content.conference.id'), nullable=False)
    created       = Column(DateTime(timezone=True))
    modified      = Column(DateTime(timezone=True))

    conference = relationship('Conference', back_populates='tracks')
    sessions   = relationship('Session', back_populates='track')


class Speaker(Base):
    __tablename__ = 'speaker'
    __table_args__ = {'schema': 'content'}

    id       = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name     = Column(String(255), nullable=False)
    bio      = Column(Text, default='')
    created  = Column(DateTime(timezone=True))
    modified = Column(DateTime(timezone=True))

    sessions = relationship('Session', secondary='content.session_speaker', back_populates='speakers')


class Session(Base):
    __tablename__ = 'session'
    __table_args__ = {'schema': 'content'}

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title       = Column(String(255), nullable=False)
    description = Column(Text, default='')
    starts_at   = Column(DateTime(timezone=True), nullable=False)
    capacity    = Column(Integer, default=0)
    track_id    = Column(UUID(as_uuid=True), ForeignKey('content.track.id'), nullable=False)
    created     = Column(DateTime(timezone=True))
    modified    = Column(DateTime(timezone=True))

    track    = relationship('Track', back_populates='sessions')
    speakers = relationship('Speaker', secondary='content.session_speaker', back_populates='sessions')
    registrations = relationship('Registration', back_populates='session')


class SessionSpeaker(Base):
    __tablename__ = 'session_speaker'
    __table_args__ = (
        UniqueConstraint('session_id', 'speaker_id', name='unique_session_speaker'),
        {'schema': 'content'}
    )

    session_id = Column(UUID(as_uuid=True), ForeignKey('content.session.id'), primary_key=True)
    speaker_id = Column(UUID(as_uuid=True), ForeignKey('content.speaker.id'), primary_key=True)


class Registration(Base):
    __tablename__ = 'registration'
    __table_args__ = (
        UniqueConstraint('user_id', 'session_id', name='unique_user_session'),
        {'schema': 'content'}
    )

    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id       = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    session_id    = Column(UUID(as_uuid=True), ForeignKey('content.session.id'), nullable=False)
    registered_at = Column(DateTime(timezone=True))
    created       = Column(DateTime(timezone=True))
    modified      = Column(DateTime(timezone=True))

    session = relationship('Session', back_populates='registrations')
