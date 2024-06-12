"""Conftest module for the movies_app tests module."""

import os
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from movies_app.models import DeclarativeBase
from sqlalchemy.orm.session import close_all_sessions


@pytest.fixture(scope="module")
def db_dependency():
    engine = create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
    Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    session = Session()

    DeclarativeBase.metadata.create_all(bind=session.get_bind())

    yield session

    close_all_sessions()
    # Drop all tables after the test
    DeclarativeBase.metadata.drop_all(bind=session.get_bind())
