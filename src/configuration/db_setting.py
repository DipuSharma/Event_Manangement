from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.configuration.settings import setting

DATABASE_URL = setting.POSTGRES_SQL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    """Initialize the database."""
    if engine:
        try:
            Base.metadata.create_all(engine)
        except Exception as e:
            print(f"Database connection failed {e}")
    else:
        raise ValueError("engine not generated")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
