import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery_app = Celery(
    "config"
)  # указываем модуль настроек для Джанго (директория config нашего проекта)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object(
    "django.conf:settings", namespace="CELERY"
)  # позволяет вносить изменения в celery через файл settings

# Load task modules from all registered Django apps.
celery_app.autodiscover_tasks()  # помогает в дальнейшем использовать декоратор celery_app, а функция будет распознаваться, как задача, которую можно будет запускать в фоновом режиме.  #noqa
