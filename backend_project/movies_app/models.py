
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, validates, declarative_base
from sqlalchemy.schema import CheckConstraint


class Base:
    """Base model class for resources."""

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


DeclarativeBase = declarative_base(cls=Base)


class Actor(DeclarativeBase):
    """Actor model class."""

    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    # an actor can not have a movie
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)
    movie = relationship("Movie", back_populates="actors", uselist=False)


class Movie(DeclarativeBase):
    """Movie model class."""

    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    actors: Mapped[list["Actor"]] = relationship("Actor", back_populates="movie", uselist=True)
    review: Mapped["Review"] = relationship(
        "Review", back_populates="movie", uselist=False, cascade="all, delete-orphan"
    )


class Review(DeclarativeBase):
    """Review model class."""

    __tablename__ = 'reviews'
    __table_args__ = (
        CheckConstraint('grade >= 1 AND grade <= 5', name='grade_range_check'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    grade = Column(Integer, nullable=False)
    # unique param is to inforce 1o1 relationship
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False, unique=True)

    # Relationship to link back to the movie
    movie: Mapped["Movie"] = relationship("Movie", back_populates="review")

    @validates('grade')
    def validate_grade(self, key, grade):
        if not isinstance(grade, int) or grade < 1 or grade > 5:
            raise ValueError("Grade must be an integer between 1 and 5.")
        return grade

# Note: in case of using many to many between movies and actors, we can use the following table

# movie_actor_association = Table(
#     'movie_actor', Base.metadata,
#     Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
#     Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True)
# )

# with relationship like so :
# actors = relationship("Actor", secondary=movie_actor_association, back_populates="movies")
# movies = relationship("Movie", secondary=movie_actor_association, back_populates="actors")
