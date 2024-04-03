from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    documento = models.CharField(max_length=100)
    codigo_pais = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    #nacimiento = models.DateField

class Titulo(models.Model):
    nombre = models.CharField(max_length=100)

class UsuarioTitulo(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)