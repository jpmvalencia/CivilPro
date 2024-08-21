from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    documento = models.CharField(max_length=100)
    codigo_pais = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    #nacimiento = models.DateField

    def __str__(self):
        return self.first_name + " " + self.last_name if (self.username != 'admin') else 'admin'
    
class Constructora(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=50, unique = True)
    contraseña = models.CharField(max_length=20)
    nit = models.CharField(max_length=100)
    codigo_pais = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre + " " + self.nit if (self.correo != 'admin') else 'admin'
    

class Titulo(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class UsuarioTitulo(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_usuario.username + " - " + self.id_titulo.nombre