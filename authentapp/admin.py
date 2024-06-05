from django.contrib import admin
from .models import Usuario, Titulo, UsuarioTitulo#, Constructora

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Titulo)
admin.site.register(UsuarioTitulo)
#admin.site.register(Constructora)