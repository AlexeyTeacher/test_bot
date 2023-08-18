from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DB_URL, logger

from models import Base

ENGINE = create_engine(DB_URL, pool_pre_ping=True)
Base.metadata.bind = ENGINE
session = scoped_session(sessionmaker(bind=ENGINE))


@contextmanager
def session_scope():
    session = sessionmaker(bind=ENGINE)()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f'session failed {e}')
        raise
    finally:
        session.close()
