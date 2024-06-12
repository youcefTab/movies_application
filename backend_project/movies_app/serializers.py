"""Serializers."""

from rest_framework import serializers
from movies_app.models import Actor, Movie, Review
from rest_framework.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

class ActorSerializer(serializers.Serializer):
    """Actor serializer class."""

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    movie_id = serializers.IntegerField(allow_null=True, required=False)

    def create(self, validated_data):
        """Create a new actor."""

        actor = Actor(**validated_data)
        self.context['session'].add(actor)
        self.context['session'].commit()

        return actor

    def update(self, instance, validated_data):
        """Update an actor."""

        for key, value in validated_data.items():
            setattr(instance, key, value)
        self.context['session'].commit()

        return instance


class ReviewSerializer(serializers.Serializer):
    """Review serializer class."""

    id = serializers.IntegerField(read_only=True)
    grade = serializers.IntegerField()
    movie_id = serializers.IntegerField()

    def validate_grade(self, value):
        """Validate the grade field to be between 1 and 5."""

        if not (1 <= value <= 5):
            raise ValidationError("Grade must be between 1 and 5.")
        return value


    def create(self, validated_data):
        """Create a new review."""

        session = self.context['session']
        movie_id = validated_data.get('movie_id')

        try:
            session.query(Movie).filter_by(id=movie_id).one()
        except NoResultFound:
            raise ValidationError({'movie_id': f"Movie with id {movie_id} does not exist."})

        review = Review(**validated_data)
        session.add(review)

        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            if isinstance(e.orig, UniqueViolation) or "reviews_movie_id_key" in str(e.orig):
                raise ValidationError({'movie_id': f"Review for movie with id {review.movie_id} already exists."})
            else:
                raise ValidationError({"detail": "An error occurred while saving the review."})

        return review

    def update(self, instance, validated_data):
        """Update a review."""

        session = self.context['session']

        for key, value in validated_data.items():
            setattr(instance, key, value)

        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise ValidationError({'movie_id': f"Review for movie with id {instance.movie_id} already exists."})
            raise e  # Re-raise if it's some other integrity error

        return instance


class MovieSerializer(serializers.Serializer):
    """Movie serializer class."""

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500)
    actors = ActorSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=False, read_only=True)


    def create(self, validated_data):
        """Create a new movie."""

        movie = Movie(**validated_data)
        self.context['session'].add(movie)
        self.context['session'].commit()

        return movie

    def update(self, instance, validated_data):
        """Update a movie."""

        for key, value in validated_data.items():
            setattr(instance, key, value)
        self.context['session'].commit()

        return instance
