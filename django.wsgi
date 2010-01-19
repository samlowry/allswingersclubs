import os
import sys

os.environ['PYTHON_EGG_CACHE'] = '/home/httpd/.python-eggs'
sys.path.append('/home/lowry/www/allswingersclubs.org')
os.environ['DJANGO_SETTINGS_MODULE'] = 'allswingersclubs.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()