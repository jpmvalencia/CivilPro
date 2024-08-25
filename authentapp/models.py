from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractUser

# class UsuarioManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('El usuario debe tener un nombre de usuario')
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(username, password, **extra_fields)

# class ConstructoraManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('La constructora debe tener un nombre de usuario')
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    country_code = models.CharField(max_length=10)
    is_employee = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doc = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.firstname + self.lastname

class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nit = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

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
    

class Degree(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class EmployeeDegree(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.username + " - " + self.degree.name