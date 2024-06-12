from rest_framework import status

from movies_app.models import Actor, Movie, Review


class TestActorViews:
    def test_get_actors(self, api_client, actors_fixture):
        response = api_client.get('/movies-app/actors/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == len(actors_fixture)

    def test_create_actor_success(self, api_client, db_dependency):
        actor_data = {
            "firstName": "John",
            "lastName": "Doe",
        }
        response = api_client.post('/movies-app/actors/', data=actor_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        # TODO - Check how to setup the renderer to return camelCase in tests
        assert response.data['first_name'] == 'John'
        assert response.data['last_name'] == 'Doe'

        actor = db_dependency.query(Actor).filter(Actor.id == response.data['id']).first()
        db_dependency.delete(actor)
        db_dependency.commit()

    def test_create_actor_missing_first_name(self, api_client):
        actor_data = {
            "lastName": "Doe"
        }
        response = api_client.post('/movies-app/actors/', data=actor_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_actor_missing_last_name(self, api_client):
        actor_data = {
            "firstName": "John"
        }
        response = api_client.post('/movies-app/actors/', data=actor_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_one_actor(self, api_client, actors_fixture):
        actor = actors_fixture[0]
        response = api_client.get(f'/movies-app/actors/{actor.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == actor.first_name
        assert response.data['last_name'] == actor.last_name

    def test_get_one_actor_does_not_exist(self, api_client):
        response = api_client.get(f'/movies-app/actors/10000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_actor_success(self, api_client, actors_fixture):
        actor = actors_fixture[0]
        actor_data = {
            "firstName": "Changed First Name",
            "lastName": "Changed Last Name"
        }
        response = api_client.put(f'/movies-app/actors/{actor.id}/', data=actor_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == "Changed First Name"
        assert response.data['last_name'] == "Changed Last Name"

    def test_update_actor_does_not_exist(self, api_client):
        actor_data = {
            "firstName": "Changed First Name",
            "lastName": "Changed Last Name"
        }
        response = api_client.put(f'/movies-app/actors/10000/', data=actor_data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_actor_success(self, api_client, db_dependency):
        actor = Actor(first_name='John', last_name='Doe')
        db_dependency.add(actor)
        db_dependency.commit()
        response = api_client.delete(f'/movies-app/actors/{actor.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert db_dependency.query(Actor).filter(Actor.id == actor.id).first() is None

    def test_delete_actor_does_not_exist(self, api_client):
        response = api_client.delete(f'/movies-app/actors/10000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestMovieViews:
    def test_get_movies(self, api_client, movies_fixture, actors_fixture, reviews_fixture):
        response = api_client.get('/movies-app/movies/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == len(movies_fixture)
        # to check if the actors and review relationships are returned in the response
        assert response.data['results'][0]['actors'][0]['first_name'] == actors_fixture[0].first_name
        assert response.data['results'][0]['review']["grade"] == reviews_fixture[0].grade

    def test_create_movie_success(self, api_client, db_dependency):
        movie_data = {
            "title": "New Movie",
            "description": "A new movie description"
        }
        response = api_client.post('/movies-app/movies/', data=movie_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Movie'
        assert response.data['description'] == 'A new movie description'

        movie = db_dependency.query(Movie).filter(Movie.id == response.data['id']).first()
        db_dependency.delete(movie)
        db_dependency.commit()

    def test_create_movie_missing_title(self, api_client):
        movie_data = {
            "description": "A new movie description"
        }
        response = api_client.post('/movies-app/movies/', data=movie_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_movie_missing_description(self, api_client):
        movie_data = {
            "title": "New Movie"
        }
        response = api_client.post('/movies-app/movies/', data=movie_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_one_movie(self, api_client, movies_fixture, actors_fixture, reviews_fixture):
        movie = movies_fixture[0]
        response = api_client.get(f'/movies-app/movies/{movie.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == movie.title
        assert response.data['description'] == movie.description
        assert response.data['actors'][0]['first_name'] == actors_fixture[0].first_name
        assert response.data['review']["grade"] == reviews_fixture[0].grade

    def test_get_one_movie_does_not_exist(self, api_client):
        response = api_client.get(f'/movies-app/movies/10000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_movie_success(self, api_client, movies_fixture):
        movie = movies_fixture[0]
        movie_data = {
            "title": "Changed Title",
            "description": "Changed Description"
        }
        response = api_client.put(f'/movies-app/movies/{movie.id}/', data=movie_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == "Changed Title"
        assert response.data['description'] == "Changed Description"

    def test_update_movie_does_not_exist(self, api_client):
        movie_data = {
            "title": "Changed Title",
            "description": "Changed Description"
        }
        response = api_client.put(f'/movies-app/movies/10000/', data=movie_data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_movie_success(self, api_client, db_dependency):
        movie = Movie(title='Test Movie', description='Test Description')
        db_dependency.add(movie)
        db_dependency.commit()
        response = api_client.delete(f'/movies-app/movies/{movie.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert db_dependency.query(Movie).filter(Movie.id == movie.id).first() is None

    def test_delete_movie_with_actors(self, api_client, db_dependency):
        movie = Movie(title='Test Movie', description='Test Description')
        actor = Actor(first_name='John', last_name='Doe', movie=movie)
        db_dependency.add(movie)
        db_dependency.add(actor)
        db_dependency.commit()

        movie_id = movie.id

        response = api_client.delete(f'/movies-app/movies/{movie_id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert db_dependency.query(Movie).filter(Movie.id == movie_id).first() is None
        assert db_dependency.query(Actor).filter(Actor.id == actor.id).first() is not None  # Actor should not be deleted

        db_dependency.delete(actor)
        db_dependency.commit()

    def test_delete_movie_with_reviews(self, api_client, db_dependency):
        movie = Movie(title='Test Movie', description='Test Description')
        review = Review(grade=5, movie=movie)
        db_dependency.add(movie)
        db_dependency.add(review)
        db_dependency.commit()

        review_id = review.id
        movie_id = movie.id

        response = api_client.delete(f'/movies-app/movies/{movie_id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert db_dependency.query(Movie).filter(Movie.id == movie_id).first() is None
        assert db_dependency.query(Review).filter(Review.id == review_id).first() is None  # both deleted

    def test_delete_movie_does_not_exist(self, api_client):
        response = api_client.delete(f'/movies-app/movies/10000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

class TestReviewViews:
    def test_get_reviews(self, api_client, reviews_fixture):
        response = api_client.get('/movies-app/reviews/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == len(reviews_fixture)

    def test_create_review_success(self, api_client, db_dependency, movies_fixture):
        db_dependency.commit()

        review_data = {
            "movieId": movies_fixture[2].id,
            "grade": 4
        }
        response = api_client.post('/movies-app/reviews/', data=review_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['grade'] == 4

        review = db_dependency.query(Review).filter(Review.id == response.data['id']).first()
        db_dependency.delete(review)
        db_dependency.commit()

    def test_create_review_missing_grade(self, api_client):
        review_data = {
            "movie_id": 1
        }
        response = api_client.post('/movies-app/reviews/', data=review_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_review_missing_movie_id(self, api_client):
        review_data = {
            "grade": 5
        }
        response = api_client.post('/movies-app/reviews/', data=review_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_review_invalid_grade(self, api_client, movies_fixture):
        review_data = {
            "grade": 6,
            "movie_id": movies_fixture[0].id
        }
        response = api_client.post('/movies-app/reviews/', data=review_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_one_review(self, api_client, reviews_fixture):
        review = reviews_fixture[0]
        response = api_client.get(f'/movies-app/reviews/{review.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['grade'] == review.grade

    def test_get_one_review_does_not_exist(self, api_client):
        response = api_client.get(f'/movies-app/reviews/10000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_review_success(self, api_client, reviews_fixture):
        review = reviews_fixture[0]
        review_data = {
            "grade": 3,
            "movieId": review.movie_id
        }
        response = api_client.put(f'/movies-app/reviews/{review.id}/', data=review_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['grade'] == 3

    def test_update_review_does_not_exist(self, api_client):
        review_data = {
            "grade": 3,
        }
        response = api_client.put(f'/movies-app/reviews/10000/', data=review_data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_review_success(self, api_client, db_dependency):
        movie = Movie(title="New Movie", description="New Description")
        review = Review(grade=5, movie=movie)
        db_dependency.add(movie)
        db_dependency.add(review)
        db_dependency.commit()

        movie_id = movie.id
        response = api_client.delete(f'/movies-app/reviews/{review.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert db_dependency.query(Review).filter(Review.id == review.id).first() is None
        db_movie = db_dependency.query(Movie).filter(Movie.id == movie_id).first()
        assert db_movie is not None

        db_dependency.delete(db_movie)
        db_dependency.commit()

    def test_delete_review_does_not_exist(self, api_client):
        response = api_client.delete(f'/movies-app/reviews/10000/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
