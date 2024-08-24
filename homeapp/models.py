from django.db import models

from authentapp.models import Usuario, Constructora

# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=50, default='Etapa Inicial')
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    constructora = models.ForeignKey(Constructora, on_delete=models.CASCADE)  # Cambio aquí

    def __str__(self):
        return self.nombre


class ProyectoUsuario(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return  self.id_proyecto.nombre + " - " + self.id_usuario.username
    

class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    presupuesto = models.FloatField()
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nombre