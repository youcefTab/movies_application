"""Customer renderers."""

from rest_framework.renderers import JSONRenderer
import inflection

class CamelCaseJSONRenderer(JSONRenderer):
    """
    Custom renderer to convert response keys to camelCase.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Render function to convert snake_case keys to camelCase."""

        camel_case_data = self._convert_keys(data)
        return super().render(camel_case_data, accepted_media_type, renderer_context)

    def _convert_keys(self, data):
        """Convert snake_case keys to camelCase."""

        if isinstance(data, dict):
            return {inflection.camelize(key, False): self._convert_keys(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._convert_keys(item) for item in data]
        else:
            return data