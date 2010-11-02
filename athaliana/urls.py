from django.conf.urls.defaults import *

urlpatterns = patterns('bao.athaliana.views',
    (r'^$', 'index'),
    (r'^query$', 'query'),
    (r'^methods$', 'methods'),
    (r'^contact$', 'contact'),
    (r'^autocomplete$', 'autocomplete'),
    (r'^simple.png$', 'simple'),
)
