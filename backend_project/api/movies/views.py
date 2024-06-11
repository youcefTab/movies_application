import os

from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def get_env_vars(request):
    env_vars_dict = dict(os.environ)
    return Response(env_vars_dict)
