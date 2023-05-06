import sqlalchemy.exc
from sqlalchemy.orm import Session
from contextlib import contextmanager
from dbs_assignment.config import engine
from fastapi import APIRouter, HTTPException

router = APIRouter()


@contextmanager
def session_scope():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def sql_execution(fetching, deleteFlag=False):
    try:
        with engine.connect() as conn:
            result = conn.execute(fetching)
            conn.commit()
            if deleteFlag is True:
                return result.rowcount
    except sqlalchemy.exc.DataError:
        raise HTTPException(status_code=400)
    return result.fetchone()
