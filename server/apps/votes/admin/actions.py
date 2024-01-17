from ..models import Event, Vote, VotingOption


def create_event_from_template(modeladmin, request, queryset):
    for template_event in queryset:
        # Создание нового мероприятия на основе шаблона
        new_event = Event(
            title=template_event.title,
            status=template_event.status,
            start_date=template_event.start_date,
        )
        new_event.save()

        # Создание голосований для нового мероприятия на основе шаблонов голосований
        for template_vote in template_event.template_votes.all():
            new_vote = Vote(
                event=new_event,
                title=template_vote.title,
                description=template_vote.description,
                status=template_vote.status,
                start_date=template_vote.start_date,
                image=template_vote.image,
            )
            new_vote.save()

            # Создание вариантов ответов для каждого голосования
            for template_option in template_vote.template_options.all():
                VotingOption(
                    vote=new_vote,
                    title=template_option.title,
                ).save()


create_event_from_template.short_description = "Создать мероприятие на основе шаблона"
