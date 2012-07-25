from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'casterly.views.home', name='home'),
    url(r'^banking/', include('money.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
