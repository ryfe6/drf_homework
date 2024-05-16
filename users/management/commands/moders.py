from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.contrib.auth.models import Permission
from users.models import User


class Command(BaseCommand):
    """Скрипт для создания группы модератора в админке."""
    def handle(self, *args, **options):
        moders_group, created = Group.objects.get_or_create(name='moders')

        # Введите _email пользователя, который будет наделен правами модератора
        _email = "admin_2@ryfe.pro"
        print("Группа moders создана")

        user = User.objects.get(email=_email)
        user.groups.add(moders_group)
