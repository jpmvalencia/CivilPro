from django.db import models

from authentapp.models import Usuario

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=50, default='Etapa Inicial')
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    constructora = models.ForeignKey(Usuario, on_delete=models.CASCADE)