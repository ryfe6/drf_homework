from django.db import models
from django.contrib.auth.models import AbstractUser
from ims.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=20, verbose_name="Телефон", help_text="Введите номер", **NULLABLE
    )
    city = models.CharField(
        max_length=50, verbose_name="Город", help_text="Укажите город", **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="user/avatars",
        verbose_name="Аватар",
        help_text="Добавьте аватар",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payment(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", **NULLABLE
    )
    payment_date = models.DateTimeField(verbose_name="дата", **NULLABLE)
    payment_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="оплаченный курс", **NULLABLE
    )
    payment_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="оплаченный предмет", **NULLABLE
    )
    payment_sum = models.PositiveIntegerField(verbose_name="сумма оплаты", **NULLABLE)
    payment_method = models.CharField(max_length=100, verbose_name="способ оплаты")

    def __str__(self):

        return f"{self.payment_course} {self.payment_lesson}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
