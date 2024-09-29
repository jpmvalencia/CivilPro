from django.contrib import admin
from homeapp.models import Project, ProjectEmployee, Role, Task, StatusTask

admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Task)
admin.site.register(ProjectEmployee)
admin.site.register(StatusTask)

