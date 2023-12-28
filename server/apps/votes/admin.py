from django.contrib import admin
from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status', 'start_date']


@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'invite_code', 'event']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'start_date', 'event', 'image']


@admin.register(VotingOption)
class VotingOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'vote']


@admin.register(VotingAnswer)
class VotingAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'vote', 'option', 'member']
