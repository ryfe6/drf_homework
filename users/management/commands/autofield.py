from django.core.management import BaseCommand

from users.models import User, Payment
from ims.models import Course, Lesson

from django.db import connection
import json


class Command(BaseCommand):
    """Класс для работы с БД приложения users и ims."""

    @staticmethod
    def json_read_course():
        """Staticmethod считывает данные из json файла с курсами."""
        with open("fixtures/course.json", "r") as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_lesson():
        """Staticmethod считывает данные из json файла с уроками."""
        with open("fixtures/lesson.json", "r") as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_user():
        """Staticmethod считывает данные из json файла с пользователями."""
        with open("fixtures/user.json", "r") as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_payment():
        """Staticmethod считывает данные из json файла с платежами."""
        with open("fixtures/payment.json", "r") as file:
            data = json.load(file)
        return data

    # Здесь мы получаем данные из фикстурв с продуктами

    def handle(self, *args, **options):
        """Функция очищает БД и записывает новые данные из фикстуры."""
        Course.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("""ALTER SEQUENCE ims_course_id_seq RESTART WITH 1""")
        self.stdout.write(self.style.SUCCESS("Курсы успешно удалены"))
        Lesson.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("""ALTER SEQUENCE ims_lesson_id_seq RESTART WITH 1""")
        self.stdout.write(self.style.SUCCESS("Уроки успешно удалены"))
        Payment.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("""ALTER SEQUENCE users_payment_id_seq RESTART WITH 1""")
        self.stdout.write(self.style.SUCCESS("Пользователи успешно удалены"))
        User.objects.all().delete()
        with connection.cursor() as cursor:
            cursor.execute("""ALTER SEQUENCE users_user_id_seq RESTART WITH 1""")
        self.stdout.write(self.style.SUCCESS("Платежи успешно удалены"))

        # Создайте списки для хранения объектов
        course_for_create = []
        lesson_for_create = []
        users_for_create = []
        payment_for_create = []

        # Обходим все значения курсов из фиктсуры для получения информации об одном объекте
        for course in Command.json_read_course():
            course_for_create.append(
                Course(
                    name=course["fields"]["name"],
                    img=course["fields"]["img"],
                    description=course["fields"]["description"],
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Course.objects.bulk_create(course_for_create)

        self.stdout.write(self.style.SUCCESS("Курсы успешно созданы"))

        # Обходим все значения уроков из фиктсуры для получения информации об одном объекте
        for lesson in Command.json_read_lesson():
            lesson_for_create.append(
                Lesson(
                    name=lesson["fields"]["name"],
                    course=Course.objects.get(pk=lesson["fields"]["course"]),
                    description=lesson["fields"]["description"],
                    img=lesson["fields"]["img"],
                    url=lesson["fields"]["url"],
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Lesson.objects.bulk_create(lesson_for_create)

        self.stdout.write(self.style.SUCCESS("Уроки успешно созданы в БД"))

        # Обходим все значения пользователей из фиктсуры для получения информации об одном объекте
        user = User.objects.create(
            email="admin@ryfe.pro",
            first_name="Denis",
            last_name="koptelev",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password("00000000")
        user.save()

        self.stdout.write(self.style.SUCCESS("Пользователи успешно созданы в БД"))

        # Обходим все данные с платежами из фиктсуры для получения информации об одном объекте
        for payment in Command.json_read_payment():
            payment_for_create.append(
                Payment(
                    user=User.objects.get(pk=payment["fields"]["user"]),
                    payment_date=payment["fields"]["payment_date"],
                    payment_course=Course.objects.get(
                        pk=payment["fields"]["payment_course"]
                    ),
                    payment_lesson=Lesson.objects.get(
                        pk=payment["fields"]["payment_lesson"]
                    ),
                    payment_sum=payment["fields"]["payment_sum"],
                    payment_method=payment["fields"]["payment_method"],
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Payment.objects.bulk_create(payment_for_create)

        self.stdout.write(self.style.SUCCESS("Платежи успешно созданы в БД"))
