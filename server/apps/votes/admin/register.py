from django.contrib import admin as django_admin

from .actions import create_event_from_template
from .forms import EventAdminForm
from .inlines import *
from ..models import *
from django.utils.html import format_html
from django.urls import reverse

from ....handlers.generators import generate_invite_code


@django_admin.register(Event)
class EventAdmin(django_admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date', 'vote_admin_link', 'member_admin_link')
    form = EventAdminForm
    inlines = [EventMemberInline, EventVotesInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # унаследованное сохранение

        # здесь происходит добавление новых участников в случае, если в форме было указано количество
        num_members = form.cleaned_data.get('num_members_to_generate')
        if num_members:
            for _ in range(num_members):
                EventMember.objects.create(
                    event=obj,
                    invite_code=generate_invite_code()
                )

    def vote_admin_link(self, obj):
        url = reverse('admin:votes_vote_changelist')  # замените appname на имя вашего приложения
        return format_html('<a href="{}?event__id={}">Администрирование голосований</a>', url, obj.id)

    vote_admin_link.short_description = 'Голосования'

    def member_admin_link(self, obj):
        url = reverse('admin:votes_eventmember_changelist')  # замените appname на имя вашего приложения
        return format_html('<a href="{}?event__id={}">Администрирование участников</a>', url, obj.id)

    member_admin_link.short_description = 'Участники'


@django_admin.register(EventMember)
class EventMemberAdmin(django_admin.ModelAdmin):
    list_display = ['invite_code', 'event']
    list_filter = ['event']


@django_admin.register(Vote)
class VoteAdmin(django_admin.ModelAdmin):
    list_display = ['title', 'description', 'status', 'start_date', 'event', 'image']
    list_filter = ['event']
    inlines = [VoteOptionsInline]


@django_admin.register(VotingOption)
class VotingOptionAdmin(django_admin.ModelAdmin):
    list_display = ['title', 'vote', 'count_votes']
    list_filter = ['vote__event', 'vote']
    readonly_fields = ['count_votes']


@django_admin.register(VotingAnswer)
class VotingAnswerAdmin(django_admin.ModelAdmin):
    list_display = ['vote', 'option', 'member']


@django_admin.register(TemplateEvent)
class TemplateEventAdmin(django_admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date')
    inlines = [TemplateEventVotesInline]
    actions = [create_event_from_template]


@django_admin.register(TemplateVote)
class TemplateVoteAdmin(django_admin.ModelAdmin):
    list_display = ['title', 'description', 'status', 'start_date', 'event', 'image']
    list_filter = ['event__title']
    inlines = [TemplateVoteOptionsInline]


@django_admin.register(TemplateVotingOption)
class TemplateVotingOptionAdmin(django_admin.ModelAdmin):
    list_display = ['title', 'vote']
    list_filter = ['vote__event__title', 'vote__title']
