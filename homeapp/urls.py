from django.urls import path

from . import views


urlpatterns = [
    path('', views.home),
    path('proyectos/', views.proper yectos_info, name='proyectos'),
    path('nuevo-proyecto/', views.nuevo_proyecto, name='nuevo-proyecto'),
    path('perfil-u/', views.perfil_usuario, name='perfil-usuario'),
]
