from django.urls import path

from . import views


urlpatterns = [
    path('', views.home),
    path('proyectos/', views.proyectos_info, name='proyectos'),
    path('nuevo-proyecto/', views.nuevo_proyecto, name='nuevo-proyecto'),
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('buscar-usuario/', views.buscar_usuario, name='buscar-usuario'),
    path('agregar-usuario/', views.agregar_usuario, name='agregar-usuario'),
    path('nueva-tarea/<int:id_proyecto>', views.nueva_tarea, name='nueva-tarea'),
    path('eliminar-proyecto/<int:id_proyecto>/', views.eliminar_proyecto, name='eliminar_proyecto')

]





