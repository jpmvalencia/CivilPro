from django.urls import path

from . import views


urlpatterns = [
    path('', views.home),
    path('proyectos/', views.proyectos_info, name='proyectos'),
    path('nuevo-proyecto/', views.nuevo_proyecto, name='nuevo-proyecto'),
]
