from datetime import datetime, timedelta

import pytz
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from ims.models import Course, Subscription
from users.models import User


@shared_task
def check_update(course_id, course_name):
    """Если курс был обновлен отправляется сообщение подписчикам курса."""
    subscription = Subscription.objects.filter(course=course_id)
    email_list = subscription.values_list('user__email', flat=True)
    send_mail(
        subject=f"Курс {course_name} получил обновление",
        message=f"Курс {course_name} был обновлен. Зайдите на платформу, чтобы ознакомиться с изменениями.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
    )


@shared_task
def check_login():
    """Если пользователь не заходил на платформу больше 30 дней, он автоматически блокируется."""
    zone = pytz.timezone(settings.TIME_ZONE)
    users = User.objects.filter(is_active=True)
    if users.exists():
        for user in users:
            try:
                # Проверяем, что last_login не None
                if user.last_login and (datetime.now(zone) - user.last_login.astimezone(zone)) > timedelta(days=30):
                    user.is_active = False
                    user.save()
            except TypeError:
                # Устанавливаем текущее время, если last_login отсутствует
                user.last_login = datetime.now()
                user.save()
