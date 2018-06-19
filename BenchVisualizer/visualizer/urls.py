from django.conf.urls import url

from . import views

app_name = 'visualizer'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registerJobs/$', views.registerJobs, name='registerJobs'),
    url(r'^registerStatus/$', views.registerStatus, name='registerStatus'),
    url(r'^(?P<job_name>[A-Za-z0-9_]+)/$', views.jobDetails, name='jobDetails'),
    url(r'^(?P<job_name>[A-Za-z0-9_]+)/raw/(?P<bench_type>(specjvm|dacapo))/$', views.raw, name='raw'),
]
