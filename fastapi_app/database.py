from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from decouple import config

DATABASE_URL = (
    f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}"
    f"@{config('POSTGRES_HOST')}:{config('POSTGRES_PORT')}/{config('POSTGRES_DB')}"
        )

engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    )

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
