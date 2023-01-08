import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# host = os.environ["POSTGRES_HOST"]
# port = os.environ["POSTGRES_PORT"]
# user = os.environ["POSTGRES_USER"]
# password = os.environ["POSTGRES_PASS"]
# db = os.environ["POSTGRES_DB"]
# dbtype = "postgresql+psycopg2"
# SQLALCHEMY_DATABASE_URI = f"{dbtype}://{user}:{password }@{host}:{port}/{db}"
env = os.environ["ENVIORNMENT"]

if env == "DEV":
    SQLALCHEMY_DATABASE_URI = "sqlite:///escucharr_testing.db"
else:
    SQLALCHEMY_DATABASE_URI = "sqlite:///escucharr_prod.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = db_session()
    try:
        yield session
    finally:
        session.close()
