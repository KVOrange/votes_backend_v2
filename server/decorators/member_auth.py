from rest_framework import status
from rest_framework.response import Response

from server.apps.votes.models import EventMember
from server.errors.http_errors import HTTP_ERRORS


def member_authorization():
    """Декоратор проверки авторизации участника по токену (идентификатору)."""

    def decorator(view_function):
        def decorated_function(request, *args, **kwargs):
            token = request.headers.get('Authorization')
            member: EventMember = EventMember.objects.filter(id=token).first()
            if not member:
                return Response(data={'error': HTTP_ERRORS['unauthorized']}, status=status.HTTP_401_UNAUTHORIZED)
            request.user = member
            return view_function(request, *args, **kwargs)

        return decorated_function

    return decorator
