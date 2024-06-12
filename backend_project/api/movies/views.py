
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from movies_app.models import Actor, Movie, Review, db_session
from rest_framework import status
from movies_app.serializers import ActorSerializer, MovieSerializer, ReviewSerializer


# Pagination class to handle page and page_size parameters
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET', 'POST'])
def actor_list_create(request):
    """Function that handles, GET-ALL and POST requests for the actor Model."""

    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        query = db_session.query(Actor)
        page = paginator.paginate_queryset(query, request)
        serializer = ActorSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = ActorSerializer(data=request.data, context={'session': db_session})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def actor_detail(request, pk):
    """Function that handles, GET, PUT and DELETE requests for the actor Model."""

    actor = db_session.query(Actor).filter(Actor.id == pk).first()

    if actor is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ActorSerializer(actor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ActorSerializer(actor, data=request.data, context={'session': db_session})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        db_session.delete(actor)
        db_session.commit()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def movie_list_create(request):
    """Function that handles, GET-ALL and POST requests for the movie Model."""

    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        query = db_session.query(Movie)
        page = paginator.paginate_queryset(query, request)
        serializer = MovieSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data, context={'session': db_session})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    """Function that handles, GET, PUT and DELETE requests for the movie Model."""

    movie = db_session.query(Movie).filter(Movie.id == pk).first()
    if movie is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data, context={'session': db_session})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if movie.review:
            db_session.delete(movie.review)
        db_session.delete(movie)
        db_session.commit()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_create(request):
    """Function that handles, GET-ALL and POST requests for the review Model."""

    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        query = db_session.query(Review)
        page = paginator.paginate_queryset(query, request)
        serializer = ReviewSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, context={'session': db_session})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, pk):
    """Function that handles, GET, PUT and DELETE requests for the review Model."""

    review = db_session.query(Review).filter(Review.id == pk).first()

    if review is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data, context={'session': db_session})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        db_session.delete(review)
        db_session.commit()
        return Response(status=status.HTTP_204_NO_CONTENT)