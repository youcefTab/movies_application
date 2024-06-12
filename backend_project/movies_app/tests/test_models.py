"""Test models.py."""
import pytest
from movies_app.models import Actor, Movie, Review
from sqlalchemy.exc import IntegrityError

class TestMovieModel:
    def test_create_movie_success(self, db_dependency):
        movie = Movie(title='Test Movie', description='Test Description')
        db_dependency.add(movie)
        db_dependency.commit()

        # Check that the actor is linked to the movie
        assert movie.title == 'Test Movie'
        assert movie.description == 'Test Description'

    def test_create_movie_missing_title(self, db_dependency):
        with pytest.raises(IntegrityError):
            movie = Movie(description='Test Description')
            db_dependency.add(movie)
            db_dependency.commit()

        db_dependency.rollback()

    def test_create_movie_missing_description(self, db_dependency):
        with pytest.raises(IntegrityError):
            movie = Movie(title='Test Title')
            db_dependency.add(movie)
            db_dependency.commit()

        db_dependency.rollback()

class TestReviewModel:
    def test_create_review_success(self, db_dependency):
        movie = Movie(title='Test Movie', description='Test Description')
        review = Review(grade=5, movie=movie)
        db_dependency.add_all([movie, review])
        db_dependency.commit()

        # Check that the review is linked to the movie
        assert review.grade == 5
        assert review.movie_id == movie.id
        assert review.movie.title == 'Test Movie'

        db_dependency.delete(review)
        db_dependency.delete(movie)
        db_dependency.commit()

    def test_movie_id_for_review_is_unique(self, db_dependency):
        with pytest.raises(IntegrityError):
            movie = Movie(title='Test Movie', description='Test Description')
            review1 = Review(grade=5, movie=movie)
            review2 = Review(grade=4, movie=movie)
            db_dependency.add_all([movie, review1, review2])
            db_dependency.commit()

        db_dependency.rollback()

    def test_create_review_missing_grade(self, db_dependency):
        with pytest.raises(IntegrityError):
            movie = Movie(title='Test Movie', description='Test Description')
            review = Review(movie=movie)
            db_dependency.add(movie)
            db_dependency.add(review)
            db_dependency.commit()

        db_dependency.rollback()

    def test_create_review_missing_movie_id(self, db_dependency):
        with pytest.raises(IntegrityError):
            review = Review(grade=5)
            db_dependency.add(review)
            db_dependency.commit()

        db_dependency.rollback()

    def test_create_review_grade_out_of_range(self, db_dependency):
        with pytest.raises(ValueError):
            movie = Movie(title='Test Movie', description='Test Description')
            review = Review(grade=6, movie=movie)
            db_dependency.add_all([movie, review])
            db_dependency.commit()

        db_dependency.rollback()

class TestActorModel:
    def test_create_actor_success(self, db_dependency):
        movie = Movie(title='Test Movie', description='Test Description')
        actor = Actor(first_name='Test', last_name='Actor', movie=movie)
        db_dependency.add_all([movie, actor])
        db_dependency.commit()

        # Check that the actor is linked to the movie
        assert actor.first_name == 'Test'
        assert actor.last_name == 'Actor'
        assert actor.movie_id == movie.id
        assert actor.movie.title == 'Test Movie'
        assert movie.actors == [actor]

        db_dependency.delete(actor)
        db_dependency.delete(movie)
        db_dependency.commit()

    def test_create_actor_missing_first_name(self, db_dependency):
        with pytest.raises(IntegrityError):
            movie = Movie(title='Test Movie', description='Test Description')
            actor = Actor(last_name='Actor', movie=movie)
            db_dependency.add_all([movie, actor])
            db_dependency.commit()

        db_dependency.rollback()

    def test_create_actor_missing_last_name(self, db_dependency):
        with pytest.raises(IntegrityError):
            movie = Movie(title='Test Movie', description='Test Description')
            actor = Actor(first_name='Test', movie=movie)
            db_dependency.add_all([movie, actor])
            db_dependency.commit()

        db_dependency.rollback()