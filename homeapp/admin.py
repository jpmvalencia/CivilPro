from django.contrib import admin
from .models import Proyecto, ProyectoUsuario

# Register your models here.
admin.site.register(Proyecto)
admin.site.register(ProyectoUsuario)