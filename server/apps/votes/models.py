import uuid

from django.db import models
from django.utils import timezone


class Event(models.Model):
    DRAFT_STATUS = 1
    ACTIVE_STATUS = 2
    COMPLETE_STATUS = 3
    STATUS_CHOICES = (
        (DRAFT_STATUS, 'Черновик'),
        (ACTIVE_STATUS, 'Активно'),
        (COMPLETE_STATUS, 'Завершено')
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, verbose_name='Статус')
    start_date = models.DateTimeField(verbose_name='Дата начала', default=timezone.now)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self) -> str:
        return self.title

    def short_info(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'start_date': self.start_date,
        }

    def full_info(self) -> dict:
        data = self.short_info()
        data['votes'] = [vote.short_info() for vote in self.votes.all()]
        return data


class EventMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')
    invite_code = models.CharField(max_length=10, unique=True, verbose_name='Код приглашения')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='members', verbose_name='Мероприятие')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self) -> str:
        return self.invite_code


class Vote(models.Model):
    DRAFT_STATUS = 1
    ACTIVE_STATUS = 2
    COMPLETE_STATUS = 3
    ANSWERED_STATUS = 4

    STATUS_CHOICES = (
        (DRAFT_STATUS, 'Черновик'),
        (ACTIVE_STATUS, 'Активно'),
        (COMPLETE_STATUS, 'Завершено')
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание вопроса', default='')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, verbose_name='Статус')
    start_date = models.DateTimeField(verbose_name='Дата начала', default=timezone.now)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='Мероприятие',
    )
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосования'

    def __str__(self) -> str:
        return self.title

    def short_info(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'start_date': self.start_date,
            'image': self.image.url,
        }


class VotingOption(models.Model):
    title = models.CharField(max_length=200, verbose_name='Текст')
    vote = models.ForeignKey(
        Vote,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Голосование',
    )

    class Meta:
        verbose_name = 'Вариант ответа в голосовании'
        verbose_name_plural = 'Варианты ответа в голосовании'

    def __str__(self) -> str:
        return self.title

    def short_info(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
        }


class VotingAnswer(models.Model):
    vote = models.ForeignKey(
        Vote,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Голосование',
    )
    option = models.ForeignKey(
        VotingOption,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вариант ответа',
    )
    member = models.ForeignKey(
        EventMember,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Участник',
    )

    class Meta:
        verbose_name = 'Ответ участника'
        verbose_name_plural = 'Ответы участников'

    def __str__(self) -> str:
        return f'{self.member} {str(self.option)}'
