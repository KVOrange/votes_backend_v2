from django import forms
from ..models import Event


class EventAdminForm(forms.ModelForm):
    """Форма для поля генерации пользователей по указанному количеству"""
    num_members_to_generate = forms.IntegerField(required=False, label='Количество участников для генерации')

    class Meta:
        model = Event
        fields = '__all__'
