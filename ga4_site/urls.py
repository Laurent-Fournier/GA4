from django.contrib import admin
from django.urls import path

from ga4_viz import views, views_mostviewedpages
urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('', views.index),
    path('monthly', views.monthly),
    path('source', views.sources),
    path('trafficsource', views.trafficsources),
    path('mostviewedpages', views_mostviewedpages.page),
    path('devices', views.devices),
]
