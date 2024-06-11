from django.urls import path

from .views import get_env_vars

urlpatterns = [
    path('env/', get_env_vars),
]
