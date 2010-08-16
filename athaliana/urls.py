from django.conf.urls.defaults import *

urlpatterns = patterns('bao.athaliana.views',
    (r'^$', 'index'),
    (r'^query$', 'query'),
    (r'^autocomplete$', 'autocomplete'),
)
