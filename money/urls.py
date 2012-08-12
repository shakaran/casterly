from django.conf.urls import patterns, include, url


urlpatterns = patterns('money.views',
    url(r'^movements/$', 'movements_list', name='movements_list'),
    url(r'^movement/edit/category/$', 'inline_category_edit', name='inline_category_edit'),
    url(r'^upload/$', 'upload_estatement', name='upload_estatement'),
)