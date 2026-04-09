"""
URL configuration for CENY - Sistema de Gestão de Manutenção Industrial
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/maintenance/', include('maintenance.urls')),
]