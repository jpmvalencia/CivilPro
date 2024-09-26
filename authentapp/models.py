from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    country_code = models.CharField(max_length=10)
    is_employee = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

    def __str__(self) -> str:
        return super().__str__()


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doc = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return super().__str__()


class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nit = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return super().__str__()


class Degree(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return super().__str__()


class EmployeeDegree(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return super().__str__()
