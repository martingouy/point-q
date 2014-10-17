from django.conf.urls import patterns, url

from pointqanalysis import views

urlpatterns = patterns('',
    url(r'^$', views.analysis, name='analysis'),
    url(r'^simulations$', views.simul_manag, name='simulations'),
    url(r'^uploadxml$', views.upload_xml, name='upload_xml'),
    url(r'^ajax', views.ajax, name='ajax'),
    url(r'^testzone', views.testzone, name='testzone')
)