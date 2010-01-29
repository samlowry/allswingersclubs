import sys
import os
import os.path

os.environ['PYTHON_EGG_CACHE'] = '/home/httpd/.python-eggs'

if not os.path.dirname(__file__) in sys.path[:1]:
    sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
