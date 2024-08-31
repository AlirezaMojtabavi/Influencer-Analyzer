from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import configparser
from Models import Base, Account, Influencer, Advertise, Bot, Event, Story


config = configparser.ConfigParser()
config.read('config.ini')
connection_string = config.get('Database', 'connection_string')
engine = create_engine(
    connection_string,
    pool_size=10,  # Adjust the pool size according to your needs
    max_overflow=20,  # Adjust max overflow according to your needs
    pool_timeout=30,  # Seconds to wait before giving up on getting a connection
    pool_recycle=3600  # Recycle connections every hour
)

# Create all tables in the database
Base.metadata.create_all(engine)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
