import os
import sys

sys.path.append(os.path.dirname(__file__)+'/../')
sys.path.append(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'call.settings'
os.environ['PYTHON_EGG_CACHE'] = '/Library/WebServer/.python-eggs'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()