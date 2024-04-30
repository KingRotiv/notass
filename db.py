from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, Session


engine = create_engine("sqlite:///sqlite.db")
metadata = MetaData()


def iniciar_db():
    metadata.create_all(engine)


def session() -> Session:
    return Session(engine)


class Base(DeclarativeBase):
    metadata = metadata
