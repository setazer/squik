# -*- coding: utf-8 -*-
from contextlib import contextmanager

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    access = Column(Integer)
    limit = Column(Integer)

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', access='{self.access}')>"

class Setting(Base):
    __tablename__ = 'settings'
    setting = Column(String(30), primary_key=True)
    value = Column(String(30), nullable=False)

    def __repr__(self):
        return f"<Setting(setting='{self.setting}', value='{self.value}')>"

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# conn_string = "postgresql://{user}:{password}@{host}:{port}/{db}".format(user=DB_USER, password=DB_PASSWORD,
#                                                                          host=DB_HOST,
#                                                                          port=DB_PORT, db=DB_NAME)
try:
    conn_string = f"mysql+mysqldb://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}" \
        f":{config['DB_PORT']}/{config['DB_NAME']}"
    engine = create_engine(conn_string)
    Base.metadata.create_all(engine)
except (OperationalError, Exception):
    conn_string = "sqlite:///local.db"
    engine = create_engine(conn_string)
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()