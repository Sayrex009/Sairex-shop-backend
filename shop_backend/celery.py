import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_backend.settings.dev')
app = Celery('shop_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
