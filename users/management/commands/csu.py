from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin_2@ryfe.pro",
            first_name="Denis",
            last_name="koptelev",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password("00000000")
        user.save()
