from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from server.errors.http_errors import HTTP_ERRORS
from .schemas.members import MemberAuth
from ..models import EventMember


@csrf_exempt
@api_view(['POST'])
def member_auth_api(request: Request) -> Response:
    """Api авторизации участника голосования.

    Разрешенные HTTP методы:
    _______________________
    | POST - Получить идентификатор пользователя по коду приглашения.

    :param request: Данные запроса.
    :return: Ответ сервера.
    """

    req_body: MemberAuth = MemberAuth.model_validate(request.data)
    member: EventMember = EventMember.objects.filter(invite_code=req_body.invite_code).first()
    if not member:
        return Response(data={'error': HTTP_ERRORS['no_member']}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data={
        'token': member.id,
        'event': member.event.short_info(),
    }, status=status.HTTP_200_OK)
