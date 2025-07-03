"""
URL configuration for overwatch_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from stats.views import favicon_view, react_app_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('stats.urls')),
    # Handle missing favicon and Apple touch icons
    path('favicon.ico', favicon_view, name='favicon'),
    path('apple-touch-icon.png', favicon_view, name='apple-touch-icon'),
    path('apple-touch-icon-precomposed.png', favicon_view, name='apple-touch-icon-precomposed'),
    # Serve React frontend for all other routes
    re_path(r'^.*$', react_app_view, name='frontend'),
]

# Serve static files in both development and production
# In production, this is needed since we're using Django's runserver
from django.views.static import serve
from django.http import HttpResponse
import mimetypes
import os

def serve_static_with_correct_mime(request, path, document_root=None):
    """Serve static files with correct MIME types."""
    # Set correct MIME types
    if path.endswith('.js'):
        content_type = 'application/javascript; charset=utf-8'
    elif path.endswith('.css'):
        content_type = 'text/css; charset=utf-8'
    elif path.endswith('.json'):
        content_type = 'application/json; charset=utf-8'
    else:
        content_type, _ = mimetypes.guess_type(path)
        if not content_type:
            content_type = 'application/octet-stream'
    
    try:
        response = serve(request, path, document_root)
        response['Content-Type'] = content_type
        response['Cache-Control'] = 'public, max-age=3600'
        return response
    except:
        return HttpResponse("File not found", status=404)

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve_static_with_correct_mime, {'document_root': settings.STATIC_ROOT}),
]
