"""Модуль административной панели Django"""

from django.contrib.auth.models import User, Group
from django.contrib import admin

# Отключение отображения системных приложений Django связанных с пользователями и группами
admin.site.unregister(User)
admin.site.unregister(Group)
