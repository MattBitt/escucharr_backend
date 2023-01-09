import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ENV = os.getenv("ENVIORNMENT", "DEV")
# PYTHONPATH = os.getenv("PYTHONPATH", ".")

if ENV == "DEV":
    SQLALCHEMY_DATABASE_URI = "sqlite:///escucharr_dev.db"
    ECHO_SQL = False  # Change back to true
elif ENV == "TESTING":
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # in-memory database
    ECHO_SQL = False
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:///escucharr_prod.db"
    ECHO_SQL = False

# ONLY NEED THE "CHECK_SAME_THREAD" ARG FOR SQLITE.  REMOVE WHEN MOVING TO POSTGRES?
engine = create_engine(
    SQLALCHEMY_DATABASE_URI, echo=ECHO_SQL, connect_args={"check_same_thread": False}
)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = db_session()
    try:
        yield session
    finally:
        session.close()
