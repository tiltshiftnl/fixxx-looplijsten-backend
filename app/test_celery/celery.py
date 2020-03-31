from __future__ import absolute_import
from celery import Celery
from django.conf import settings

app = Celery('test_celery',
             broker=settings.CELERY_BROKER,
             backend='rpc://',
             include=['test_celery.tasks'])
