from django.db import models
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование курса")
    img = models.ImageField(
        verbose_name="Превью курса", upload_to="course/photo", **NULLABLE
    )
    description = models.TextField(verbose_name="Описание курса", **NULLABLE)

    author = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование урока")
    course = models.ForeignKey(
        Course, verbose_name="Наименование курса", on_delete=models.CASCADE, **NULLABLE
    )
    description = models.TextField(verbose_name="описание урока", **NULLABLE)
    img = models.ImageField(
        verbose_name="Превью урока", upload_to="lessons/photo", **NULLABLE
    )
    url = models.URLField(
        max_length=100, verbose_name="Ссылка на видеоурок", **NULLABLE
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        to="users.User", verbose_name="пользователь", on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, verbose_name="курс", on_delete=models.CASCADE)
    subscription_is = models.BooleanField(default=False, verbose_name="Признак подписки")

    def __str__(self):
        return f"Пользователь {self.user} подписан на курс {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
