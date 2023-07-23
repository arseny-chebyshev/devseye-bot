from django.db import models
from django.db.models import Q
from django.contrib.postgres import fields as pgfields
from multiselectfield import MultiSelectField


# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_bot = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, null=True)
    language_code = models.CharField(max_length=3, null=True)
    is_premium = models.BooleanField(null=True)
    added_to_attachment_menu = models.BooleanField(null=True)
    can_join_groups = models.BooleanField(default=False)
    can_read_all_group_messages = models.BooleanField(default=False)
    supports_inline_queries = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    receives_notification = models.BooleanField(default=False)
    has_blocked_bot = models.BooleanField(default=False)

    def has_settings(self):
        return hasattr(self, 'settings')


class Settings(models.Model):

    class LEVELS(models.TextChoices):
        INTERN = "Intern", "Intern"
        JUNIOR = "Junior", "Junior"
        MIDDLE = "Middle", "Middle"
        TEAM_LEAD = "Team Lead", "Team Lead"

    class EMPLOYMENT_TYPE(models.TextChoices):
        REMOTE = "Удаленная работа", "Удаленная работа"
        HYBRID = "Гибрид", "Гибрид"
        RELOCATION = "Релокация", "Релокация"
        OFFICE = "Офис", "Офис"

    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE,
                                related_name='settings')
    level = MultiSelectField(max_length=255,
                             choices=LEVELS.choices)
    employment_type = MultiSelectField(max_length=255,
                                       choices=EMPLOYMENT_TYPE.choices)
    skills = pgfields.ArrayField(models.CharField(max_length=255))
    locations = pgfields.ArrayField(models.CharField(max_length=255))

    @classmethod
    def filter_vacancy_recipients(cls, vacancy_text: str) -> list[User]:
        return [setting.user for setting in
                cls.objects.filter(
                    Q(level__contains=vacancy_text) |
                    Q(employment_type__contains=vacancy_text) |
                    Q(skills__contains=[vacancy_text]) |
                    Q(locations__contains=[vacancy_text]),
                    user__receives_notification=True)]


class TelegramChannel(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255, null=True)
