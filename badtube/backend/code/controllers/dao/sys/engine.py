# for the moment we use sqlite but after postgresql
from contextlib import contextmanager
from typing import Annotated
from fastapi import Depends
from sqlalchemy import URL, Engine
from sqlmodel import SQLModel, Session, create_engine
from settings import get_settings

def get_engine() -> Engine:
    settings = get_settings()

    if get_settings().local_db:
        sqlite_file_name = "database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"

        connect_args = {"check_same_thread": False}
        return create_engine(sqlite_url, connect_args=connect_args)
    else:
        SQLModel.metadata.schema = "fastapi"

        url = URL.create(
            "postgresql",
            host=settings.db_host,
            username=settings.db_username,
            password=settings.db_password,
            database=settings.db_name)
        return create_engine(url)

engine = get_engine()

def init_db():
    SQLModel.metadata.create_all(engine)

def clear_db():
    SQLModel.metadata.drop_all(engine)

# this is a transactionnal scope
# for sqlrequest
@contextmanager
def session_scope():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_session():
    with session_scope() as sess:
        yield sess

SessionInj = Annotated[Session, Depends(get_session)]
