# Generated by Django 5.0.4 on 2024-05-27 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ims", "0005_alter_lesson_url_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="subscription_is",
            field=models.BooleanField(default=False, verbose_name="Признак подписки"),
        ),
    ]
