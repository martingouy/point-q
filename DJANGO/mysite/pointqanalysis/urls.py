from django.conf.urls import patterns, url

from pointqanalysis import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<link1>\d+)/(?P<link2>\d+)/$', views.detail, name='detail'),
)