from django.urls import path
from .api.ping import ping


urlpatterns = [
    path('ping', ping),
]
