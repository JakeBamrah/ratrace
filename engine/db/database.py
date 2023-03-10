import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# initialize db
db_path: str = os.path.join(Path.cwd(), 'db', r'ratrace.db')
engine: Engine = create_engine(f'sqlite:///{db_path}', echo=False)
Session = scoped_session(sessionmaker(
                                    autocommit=False,
                                    autoflush=False,
                                    bind=engine))

Base = declarative_base()
Base.query = Session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from . import models
    Base.metadata.create_all(bind=engine)

class DBSessionContext:
    def __init__(self, engine):
        self.engine = engine

    def __enter__(self):
        self.session = Session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.remove()
