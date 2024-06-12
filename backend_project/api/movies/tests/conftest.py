
import pytest
import os
from movies_app.models import Actor, Movie, Review, DeclarativeBase
from rest_framework.test import APIClient
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.session import close_all_sessions


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="module")
def db_dependency():
    engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
    Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    session = Session()

    DeclarativeBase.metadata.create_all(bind=session.get_bind())

    yield session

    close_all_sessions()

    # Drop all tables after the test
    DeclarativeBase.metadata.drop_all(bind=session.get_bind())

# TODO - Debug fixture not recognized when moving this fixtures to in movies_app/tests/ (where it should be)

@pytest.fixture(scope="module")
def actors_fixture(db_dependency, movies_fixture):
    actors = [
        Actor(first_name='John', last_name='Doe', movie=movies_fixture[0]),
        Actor(first_name='Jane', last_name='Doe', movie=movies_fixture[1]),
        Actor(first_name='Alice', last_name='Smith'),
    ]
    db_dependency.add_all(actors)
    db_dependency.commit()
    yield actors

    for actor in actors:
        db_dependency.delete(actor)

    db_dependency.commit()


@pytest.fixture(scope="module")
def movies_fixture(db_dependency):
    movies = [
        Movie(title='Test Movie 1', description='Test Description 1'),
        Movie(title='Test Movie 2', description='Test Description 2'),
        Movie(title='Test Movie 3', description='Test Description 3'),
    ]
    db_dependency.add_all(movies)
    db_dependency.commit()
    yield movies

    for movie in movies:
        db_dependency.delete(movie)

    db_dependency.commit()


@pytest.fixture(scope="module")
def reviews_fixture(db_dependency, movies_fixture):
    reviews = [
        Review(grade=5, movie=movies_fixture[0]),
        Review(grade=4, movie=movies_fixture[1]),
    ]
    db_dependency.add_all(reviews)
    db_dependency.commit()
    yield reviews

    for review in reviews:
        db_dependency.delete(review)

    db_dependency.commit()
