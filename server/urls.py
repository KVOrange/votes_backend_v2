"""Глобальные URL для всего сервера"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import config

urlpatterns = [
    path(f'{config.CONFIG_FILE}', admin.site.urls),
    path('system/', include('server.apps.system.urls')),
    path('api/', include('server.apps.votes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
