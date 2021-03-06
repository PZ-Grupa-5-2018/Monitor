"""monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from monitorinterface import views

urlpatterns = [
    url(r'^hosts/$', views.HostList.as_view(),name="hosts_list"),
    url(r'^hosts/(?P<pk>[0-9]+)/$', views.HostDetail.as_view(),name="hosts_detail"),
    url(r'^hosts/(?P<name>[\w\-]+)/$', views.HostDetail.as_view()),
    url(r'^hosts/(?P<host_id>[0-9]+)/metrics/$', views.MetricList.as_view(),name="metric_list"),
    url(r'^hosts/(?P<host_name>[\w\-]+)/metrics/$', views.MetricList.as_view(), name="metric_list_name"),
    url(r'^hosts/(?P<host_id>[0-9]+)/metrics/(?P<pk>[0-9]+)/$', views.MetricDetail.as_view()),
    url(r'^hosts/(?P<host_id>[0-9]+)/metrics/(?P<type>[\w\-]+)/$', views.MetricDetail.as_view()),
    url(r'^hosts/(?P<host_name>[\w\-]+)/metrics/(?P<pk>[0-9]+)/$', views.MetricDetail.as_view(),name='metric_detail'),
    url(r'^hosts/(?P<host_name>[\w\-]+)/metrics/(?P<type>[\w\-]+)/$', views.MetricDetail.as_view()),
    url(r'^hosts/(?P<host_id>[0-9]+)/metrics/(?P<metric_id>[0-9]+)/measurements/$', views.MeasurementList.as_view(),
        name="measurement_list"),
    url(r'^hosts/(?P<host_id>[0-9]+)/metrics/(?P<metric_name>[\w\-]+)/measurements/$', views.MeasurementList.as_view(),
        name="measurement_list"),
    url(r'^hosts/(?P<host_name>[\w\-]+)/metrics/(?P<metric_id>[0-9]+)/measurements/$', views.MeasurementList.as_view(),
        name="measurement_list"),
    url(r'^hosts/(?P<host_name>[\w\-]+)/metrics/(?P<metric_name>[\w\-]+)/measurements/$', views.MeasurementList.as_view(),
        name="measurement_list"),
]

