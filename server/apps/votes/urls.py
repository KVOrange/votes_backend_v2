from django.urls import path
from .api.members import member_auth_api
from .api.event import event_api
from .api.votes import votes_api, votes_options_api
urlpatterns = [
    path('member/auth', member_auth_api),
    path('events', event_api),
    path('events/votes', votes_api),
    path('events/votes/<int:vote_id>/options', votes_options_api),
]
