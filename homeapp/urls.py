from django.urls import path

from . import views


urlpatterns = [
    path('', views.home),
    path('pr-info/', views.proyectos_info, name='proyecto-info'),
]
