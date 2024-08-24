from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractUser

class UsuarioManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class ConstructoraManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('La constructora debe tener un nombre de usuario')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class UsuarioBase(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'

    class Meta:
        abstract = True

class Usuario(UsuarioBase):
    documento_usu = models.CharField(max_length=255, unique=True, null=False, blank=False)
    nombre_usu = models.CharField(max_length=255, null=False, blank=False)
    apellido_usu = models.CharField(max_length=255, null=False, blank=False)
    telefono_usu = models.CharField(max_length=255, null=True, blank=True)
    correo_usu = models.EmailField(max_length=255, null=False, blank=False)
    codigo_pais = models.CharField(max_length=255)
    objects = UsuarioManager()

    def __str__(self):
        return self.nombre_usu

class Constructora(UsuarioBase):
    nit_con = models.CharField(max_length=255, unique=True, null=False, blank=False)
    nombre_con = models.CharField(max_length=255, null=False, blank=False)
    correo_con = models.EmailField(max_length=255, null=False, blank=False)
    telefono_con = models.CharField(max_length=255, null=True, blank=True)
    objects = ConstructoraManager()

    def __str__(self):
        return self.nombre_con

# Create your models here.
# class Usuario(AbstractUser):
#     documento = models.CharField(max_length=100)
#     codigo_pais = models.CharField(max_length=100)
#     telefono = models.CharField(max_length=20)
#     #nacimiento = models.DateField

#     def __str__(self):
#         return self.first_name + " " + self.last_name if (self.username != 'admin') else 'admin'
    
#class Constructora(models.Model):
 #   nombre = models.CharField(max_length=100)
  #  correo = models.CharField(max_length=50, unique = True)
   # contraseña = models.CharField(max_length=20)
   # nit = models.CharField(max_length=100)
   # codigo_pais = models.CharField(max_length=100)
   # telefono = models.CharField(max_length=20)

   # def __str__(self):
   #     return self.nombre + " " + self.nit if (self.correo != 'admin') else 'admin'
    

class Titulo(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class UsuarioTitulo(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_usuario.username + " - " + self.id_titulo.nombre