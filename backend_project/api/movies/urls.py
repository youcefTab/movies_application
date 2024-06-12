from django.urls import path
from .views import actor_list_create, actor_detail, movie_list_create, movie_detail, review_list_create, review_detail

urlpatterns = [
    path('movies/', movie_list_create, name='movie-list-create'),
    path('movies/<int:pk>/', movie_detail, name='movie-detail'),
    path('actors/', actor_list_create, name='actor-list-create'),
    path('actors/<int:pk>/', actor_detail, name='actor-detail'),
    path('reviews/', review_list_create, name='review-list-create'),
    path('reviews/<int:pk>/', review_detail, name='review-detail'),
]
