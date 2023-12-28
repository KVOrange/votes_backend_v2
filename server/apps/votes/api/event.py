from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.votes.models import EventMember
from server.decorators.member_auth import member_authorization


@csrf_exempt
@api_view(['GET'])
@member_authorization()
def event_api(request: Request) -> Response:
    """Api для работы с мероприятиями.

    Разрешенные HTTP методы:
    _______________________
    | GET - Получить информацию по текущему мероприятию.

    :param request: Данные запроса.
    :return: Ответ сервера.
    """

    member: EventMember = request.user

    return Response(member.event.short_info(), status=status.HTTP_200_OK)
