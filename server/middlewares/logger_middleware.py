"""Middleware связанные с логгирование."""
import logging

logger = logging.getLogger(__name__)


class HttpResponseLoggerMiddleware:
    """Middleware логгирования HTTP запросов"""

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        if response.status_code == 200:
            logger.info(f'{request.method} {request.path} {response.status_code}')
        else:
            logger.warning(f'{request.method} {request.path} {response.status_code}')
        return response
