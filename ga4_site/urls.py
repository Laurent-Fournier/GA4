from django.contrib import admin
from django.urls import path

from ga4_viz import views, views_source, views_trafficsource, views_mostviewedpages, views_devices
urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('', views.index),
    path('source', views_source.page),
    path('trafficsource', views_trafficsource.page),
    path('mostviewedpages', views_mostviewedpages.page),
    path('devices', views_devices.page),
]
