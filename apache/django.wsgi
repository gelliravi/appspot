import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from err import ExceptionMiddleware

sys.path.insert(0, '/home/bao/public_html')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bao.settings'

import django.core.handlers.wsgi

@ExceptionMiddleware
def application(environ, start_response):
    t = django.core.handlers.wsgi.WSGIHandler()
    return t(environ, start_response)

