#NOTE: Remove if using mailchimp
from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TripBuddySG.settings')

from django.conf import settings

app = Celery('proj',
             broker='amqp://',
             backend='rpc://',
             include=['TripBuddy.tasks'])


if __name__ == '__main__':
    app.start()