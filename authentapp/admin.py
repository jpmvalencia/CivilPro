from authentapp.models import Employee, EmployeeDegree, Company, CustomUser, Degree
from django.contrib import admin

admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(CustomUser)
admin.site.register(Degree)
admin.site.register(EmployeeDegree)
