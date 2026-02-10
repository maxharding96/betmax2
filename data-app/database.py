from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from contextlib import contextmanager

engine = create_engine("postgresql://user:pass@localhost/db_name", echo=True)

SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


@contextmanager
def get_session():
    """Transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
