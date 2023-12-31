"""Глобальные URL для всего сервера"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import ADMIN_PATH

urlpatterns = [
    path(f'{ADMIN_PATH}', admin.site.urls),
    path('system/', include('server.apps.system.urls')),
    path('api/', include('server.apps.votes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
