"""Custom parsers."""

from rest_framework.parsers import JSONParser
import inflection

class CamelCaseToSnakeCaseJSONParser(JSONParser):
    """
    Custom parser to convert camelCase JSON keys to snake_case.
    """

    def parse(self, stream, media_type=None, parser_context=None):
        """Parse function to convert camelCase keys to snake_case."""

        data = super().parse(stream, media_type, parser_context)
        return self._convert_keys(data)

    def _convert_keys(self, data):
        """Convert camelCase keys to snake_case."""

        if isinstance(data, dict):
            return {inflection.underscore(key): self._convert_keys(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._convert_keys(item) for item in data]
        else:
            return data
