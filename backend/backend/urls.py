"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from stats.views import favicon_view, react_app_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('stats.urls')),
    path('favicon.ico', favicon_view, name='favicon'),
    path('apple-touch-icon.png', favicon_view, name='apple-touch-icon'),
    path('apple-touch-icon-precomposed.png', favicon_view, name='apple-touch-icon-precomposed'),
    re_path(r'^.*$', react_app_view, name='frontend'),
]
