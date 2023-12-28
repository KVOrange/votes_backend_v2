from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.votes.models import EventMember, VotingAnswer
from server.decorators.member_auth import member_authorization
from server.errors.http_errors import HTTP_ERRORS
from .schemas.votes import SendVoteAnswer
from ..models import Vote


@csrf_exempt
@api_view(['GET'])
@member_authorization()
def votes_api(request: Request) -> Response:
    """Api для работы с голосованиями.

    Разрешенные HTTP методы:
    _______________________
    | GET - Получить информацию по текущему мероприятию.

    :param Request request: Данные запроса.
    :return: Ответ сервера.
    """

    member: EventMember = request.user

    answered_votes = member.answers.values_list('vote__id', flat=True)

    active_votes = [vote.short_info() for vote in member.event.votes.filter(status=Vote.ACTIVE_STATUS)]
    complete_votes = [vote.short_info() for vote in member.event.votes.filter(status=Vote.COMPLETE_STATUS)]

    for vote in active_votes:
        if vote['id'] in answered_votes:
            vote['status'] = Vote.ANSWERED_STATUS

    return Response(data={
        'active': active_votes,
        'complete': complete_votes,
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET', 'POST'])
@member_authorization()
def votes_options_api(request: Request, vote_id: int) -> Response:
    """Api для работы с ответами в голосовании.

    Разрешенные HTTP методы:
    _______________________
    | GET - Получить все варианты ответов в голосовании.
    | POST - Отправить ответ на голосование.

    :param Request request: Данные запроса.
    :param int vote_id: Идентификатор голосования.
    :return: Ответ сервера.
    """
    member: EventMember = request.user
    vote: Vote = Vote.objects.filter(id=vote_id).first()
    if not vote:
        return Response(data={'error': HTTP_ERRORS['no_vote']}, status=status.HTTP_404_NOT_FOUND)
    if vote.event != member.event:
        return Response(data={'error': HTTP_ERRORS['forbidden']}, status=status.HTTP_403_FORBIDDEN)
    if vote.status == Vote.COMPLETE_STATUS:
        return Response(data={'error': HTTP_ERRORS['forbidden']}, status=status.HTTP_406_NOT_ACCEPTABLE)
    if member.answers.filter(vote=vote).first():
        return Response(data={'error': HTTP_ERRORS['forbidden']}, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.method == 'GET':
        return Response(data=[
            option.short_info() for option in vote.options.all()
        ], status=status.HTTP_200_OK)
    if request.method == 'POST':
        req_body: SendVoteAnswer = SendVoteAnswer.model_validate(request.data)
        answer = VotingAnswer()
        answer.vote = vote
        answer.member = member
        answer.option_id = req_body.option_id
        answer.save()
        return Response()
