from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import logging
from functools import wraps


FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('dbserver')


# initialize db
db_path: str = r'ratrace.db'
engine: Engine = create_engine(f'sqlite:///{db_path}', echo=False)
session: scoped_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

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
        self.session = scoped_session(sessionmaker(autocommit=False, bind=self.engine))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.remove()

def commit_wrapper(obj_factory):
    """
    Simple decorator that wraps sqlalchemy object creation in a session context
    and attempts a commit.
    """
    @wraps(obj_factory)
    def wrapper(*args):
        with DBSessionContext(engine) as db:
            try:
                objs = obj_factory(*args)
                db.session.add_all(objs)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                logger.error(e)
                db.session.rollback()
    return wrapper

def query_wrapper(query):
    """
    Simple decorator that wraps sqlalchemy object queries in a session context.
    """
    result = []
    with DBSessionContext(engine) as db:
        try:
            result = db.session.query(query)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()

    return result
