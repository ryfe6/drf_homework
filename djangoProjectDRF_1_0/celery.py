from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# ��������� ���������� ��������� ��� �������� �������
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProjectDRF_1_0.settings')

# �������� ���������� ������� Celery
app = Celery('djangoProjectDRF_1_0')

# �������� �������� �� ����� Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# �������������� ����������� � ����������� ����� �� ������ tasks.py � ����������� Django
app.autodiscover_tasks()
