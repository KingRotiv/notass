from contextlib import asynccontextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, Session


engine = create_engine("sqlite:///sqlite.db")
metadata = MetaData()


@asynccontextmanager
async def iniciar_db(*args):
    metadata.create_all(engine)
    yield


def session() -> Session:
    return Session(engine)


class Base(DeclarativeBase):
    metadata = metadata
