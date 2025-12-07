"""
URL configuration for ga4_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ga4_viz import views, views_source, views_trafficsource

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('', views.index),
    path('source', views_source.page),
    path('trafficsource', views_trafficsource.page),
]
