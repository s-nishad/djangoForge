import os
from celery import Celery

# Set default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Create Celery app
app = Celery("config")

# Load settings from Django settings, using the "CELERY_" namespace
app.config_from_object("django.conf:settings", namespace="CELERY")


# Auto-discover tasks from all installed apps
app.autodiscover_tasks()
