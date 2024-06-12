from django.apps import AppConfig
from django.conf import settings

class MoviesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies_app'

    def ready(self):
        # Add custom parser to the REST_FRAMEWORK settings
        if 'DEFAULT_PARSER_CLASSES' in settings.REST_FRAMEWORK:
            settings.REST_FRAMEWORK['DEFAULT_PARSER_CLASSES'] = (
                'movies_app.parsers.CamelCaseToSnakeCaseJSONParser',
                *settings.REST_FRAMEWORK['DEFAULT_PARSER_CLASSES'],
            )
        else:
            settings.REST_FRAMEWORK['DEFAULT_PARSER_CLASSES'] = (
                'movies_app.parsers.CamelCaseToSnakeCaseJSONParser',
                'rest_framework.parsers.JSONParser',
            )