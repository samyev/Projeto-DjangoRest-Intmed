"""medicar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token  

from agenda.viewsets import UserViewSet, AgendaViewSet, ConsultaViewSet, HorarioViewSet

from medicos.viewsets import MedicoViewSet, EspecialidadeViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'medicos', MedicoViewSet)
router.register(r'especialidades', EspecialidadeViewSet)
router.register(r'consultas', ConsultaViewSet)
router.register(r'horarios', HorarioViewSet)
router.register(r'agendas', AgendaViewSet, basename='agendas')

#router.register(r'agendas/(?P<library_id>[0-9]+)', AgendaViewSet, basename='agendas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]

