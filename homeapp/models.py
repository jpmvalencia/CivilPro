from django.db import models
from django.db.models import Sum
from authentapp.models import CustomUser, Company, Employee

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, default='Etapa Inicial')
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.FloatField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    @property
    def remaining_budget(self):
        # Suma de los presupuestos de las tareas
        used_budget = self.tasks.aggregate(Sum('budget'))['budget__sum'] or 0
        return self.budget - used_budget
    
    
class StatusTask(models.Model):
    status = models.CharField(max_length=50, default='Pendiente')

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    inCharge = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(StatusTask, on_delete=models.CASCADE)  

    def __str__(self):
        return self.name
       
class Role(models.Model):
    name = models.CharField(max_length=100)
    
class ProjectEmployee(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return  self.project.name + " - " + self.employee.firstname + self.employee.lastname
    