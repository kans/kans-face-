import os
import sys

os.environ['DJANGO_SETTINGS_MODULE']='settings'
#os.environ["CELERY_LOADER"] = "django"

#TODO: is this safe?
path = os.path.abspath(__file__ + '/../..')
if path not in sys.path:
  sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import monitor
monitor.start(interval=1.0)