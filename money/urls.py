from django.conf.urls import patterns, include, url


urlpatterns = patterns('money.views',
    url(r'^movements/$', 'movements_list', name='movements_list'),
)