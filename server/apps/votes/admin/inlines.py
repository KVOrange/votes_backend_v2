from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from ..models import *


class BaseInline(admin.TabularInline):
    """Класс базового инлайна для моделей, которым необходима ссылка на редактирования"""
    extra = 0

    def edit_link(self, instance):
        if instance.pk:
            url = reverse('admin:%s_%s_change' % (instance._meta.app_label, instance._meta.model_name),
                          args=[instance.pk])
            return format_html('<a href="{}">Редактировать</a>', url)
        return ''

    edit_link.short_description = 'Ссылка на редактирование'
    readonly_fields = ['edit_link']


class EventMemberInline(BaseInline):
    model = EventMember


class EventVotesInline(BaseInline):
    model = Vote


class VoteOptionsInline(BaseInline):
    model = VotingOption

    def vote_option_count(self, inline):
        return inline.count_votes()

    vote_option_count.short_description = 'Количество голосов'
    readonly_fields = ['vote_option_count', 'edit_link']


class TemplateEventVotesInline(BaseInline):
    model = TemplateVote


class TemplateVoteOptionsInline(BaseInline):
    model = TemplateVotingOption
