"""Conftest module for the movies_app tests module."""

import os
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from movies_app.models import DeclarativeBase

# Define a fixture to create an engine
@pytest.fixture(scope='session')
def engine():
    # Replace with your actual PostgreSQL connection string
    return create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")

# Define a fixture to create a scoped session
@pytest.fixture(scope='session')
def db_session_factory(engine):
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@pytest.fixture(scope="module")
def db_dependency(db_session_factory):
    session = db_session_factory()
    DeclarativeBase.metadata.create_all(bind=session.get_bind())


    yield session
    session.close()
    # Drop all tables after the test
    DeclarativeBase.metadata.drop_all(bind=session.get_bind())