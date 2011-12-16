import os
import sys

os.environ['DJANGO_SETTINGS_MODULE']='settings'
#os.environ["CELERY_LOADER"] = "django"

import settings
sys.path.append(settings.ROOT_DIR)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import monitor
monitor.start(interval=1.0)