from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from edut_online import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edut_online.settings')

app = Celery('edut_online')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': "util.email_send.send_email_code",
#         'schedule': 15.0,
#         'args': ('18826138192@163.com',)
#     },
# }
app.conf.timezone = 'Asia/Shanghai'

