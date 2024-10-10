from authentapp.models import CustomUser, Employee
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from homeapp.models import Project, ProjectEmployee, Role, StatusTask, Task, Chat
from django.shortcuts import redirect


# Create your views here.


def home(request):
    return render(request, 'home.html')

@login_required
def eliminar_proyecto(request, id_proyecto):
    try:
        proyecto = Project.objects.get(id=id_proyecto)
        proyecto.delete()
        return redirect('proyectos')
    except Project.DoesNotExist:
        return redirect('proyectos')

@login_required
def eliminar_tarea(request, id_tarea):
    try:
        tarea = Task.objects.get(id=id_tarea)
        tarea.delete()
        return redirect('proyectos')
    except Project.DoesNotExist:
        return redirect('proyectos')

@login_required
def nueva_tarea(request, id_proyecto):
    proyecto = Project.objects.get(id=id_proyecto)
    
    if request.method == 'GET':
        status_list = StatusTask.objects.all()  # Obtener los estados disponibles
        return render(request, 'nueva-tarea.html', {'status_list': status_list})
    
    else:
        try:
            # Obtener los datos del formulario
            name = request.POST.get("title")
            description = request.POST.get("description")
            start_date = request.POST.get("start-date")
            end_date = request.POST.get("end-date")
            budget = request.POST.get("presupuesto")
            status_id = request.POST.get("status")
            
            # Obtener el objeto StatusTask seleccionado
            status = get_object_or_404(StatusTask, id=status_id)
            
            # Crear una nueva instancia de Task
            tarea = Task(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                budget=budget,
                project=proyecto,
                status=status  # Asignar el estado a la tarea
            )
            
            # Guardar la tarea en la base de datos
            tarea.save()
            return redirect('proyectos')  # Redirige a la página de proyectos
        
        except Exception as e:
            # Mostrar mensaje de error en caso de fallo
            status_list = StatusTask.objects.all()
            return render(request, 'nueva-tarea.html', {'error': 'Ingresa datos válidos.', 'status_list': status_list}) 


@login_required
def agregar_menssaje(request):
    if request.method == 'GET':
        project_id = request.GET.get('projectId')
        user_email = request.GET.get('userEmail')
        message = request.GET.get('message')
        
        # Obtener el proyecto
        project = Project.objects.get(id=project_id)

        # Obtener el usuario relacionado con el correo electrónico
        user = CustomUser.objects.get(email=user_email)

        # Crear y guardar el mensaje en el modelo Chat
        chat_message = Chat(project=project, employee=user, message=message)
        chat_message.save()

        # Redirigir a la página de proyectos
        return redirect('proyectos')

    return redirect('proyectos')


@login_required
def editar_tarea(request, id_tarea):
    tarea = get_object_or_404(Task, id=id_tarea)
    
    if request.method == 'POST':
         # Obtener el valor del presupuesto
        presupuesto = request.POST.get('presupuesto', '').replace(',', '.')

        # Actualizar el valor del presupuesto en el objeto tarea
        # Obtener datos del formulario
        tarea.name = request.POST.get('title')
        tarea.description = request.POST.get('description')
        tarea.start_date = request.POST.get('start-date')
        tarea.end_date = request.POST.get('end-date')
        tarea.budget = float(presupuesto)
        
        # Actualizar el estado de la tarea
        status_id = request.POST.get('status')
        status = StatusTask.objects.get(id=status_id)
        tarea.status = status
        
        # Guardar los cambios en la base de datos
        tarea.save()
        
        # Redirigir a la vista de proyectos o donde desees
        return redirect('proyectos')
    
    return redirect('proyectos')   

@login_required
def nuevo_proyecto(request):
    if request.method == "GET":
        return render(request, "nuevo-proyecto.html")
    else:
        try:
            # Obtener los datos del formulario
            name = request.POST.get("title")
            description = request.POST.get("description")
            start_date = request.POST.get("start-date")
            end_date = request.POST.get("end-date")
            budget = request.POST.get("presupuesto")

            # Obtener la instancia de la compañía del usuario
            company = request.user.company
            
            # Crear una instancia del proyecto
            proyecto = Project(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                budget=budget,
                company=company  # Pasar la instancia de la compañía, no el NIT
            )

            # Guardar el proyecto en la base de datos
            proyecto.save()
            return redirect('proyectos')  # Redirige a la página de proyectos
        except Exception as e:
            # Mostrar mensaje de error en caso de fallo
            return render(request, 'nuevo-proyecto.html', {'error': 'Ingresa datos válidos.'})

@login_required
def proyectos_info(request):
    allproyectos = Project.objects.all()
    usuario_actual = request.user
    tareas = Task.objects.all()
    roles = Role.objects.all()
    show_link = False
    usuarios = ProjectEmployee.objects.all()
    status_list = StatusTask.objects.all()

    # Obtener todos los mensajes de chat
    chat_messages = Chat.objects.all()

    if usuario_actual.is_employee:
        try:
            # Filtrar los proyectos por el usuario actual (empleado)
            proyectos = Project.objects.filter(projectemployee__employee=usuario_actual)
        except Employee.DoesNotExist:
            proyectos = []
    else:
        show_link = True
        try:
            # Filtrar los proyectos por la compañía del usuario actual (si es administrador)
            company = usuario_actual.company
            proyectos = Project.objects.filter(company=company)
        except Employee.DoesNotExist:
            proyectos = []

    # Pasar los datos al template, incluyendo los mensajes de chat
    return render(request, 'proyectos.html', {
        'proyectos': proyectos,
        'usuario_actual': usuario_actual,
        'tareas': tareas,
        'roles': roles,
        'show_link': show_link,
        'usuarios': usuarios,
        'status_list': status_list,
        'chat_messages': chat_messages  # Mensajes de chat
    })

@login_required
def actualizar_perfil(request):
    if request.method == 'POST':
        # Obtener el usuario actual
        usuario_actual = request.user

        # Obtener los datos del formulario
        nuevo_nombre = request.POST.get('first_name')
        nuevo_apellido = request.POST.get('last_name')
        nuevo_username = request.POST.get('username')
        nuevo_password = request.POST.get('password')

        # Actualizar los campos del usuario con los nuevos datos
        usuario_actual.first_name = nuevo_nombre
        usuario_actual.last_name = nuevo_apellido
        usuario_actual.username = nuevo_username
        if nuevo_password:
            usuario_actual.set_password(nuevo_password)

        # Guardar los cambios en la base de datos
        usuario_actual.save()

        # Mostrar un mensaje de éxito
        messages.success(request, 'Perfil actualizado correctamente.')

        # Redirigir a alguna página de confirmación o a la misma página
        return redirect('/proyectos')  # Reemplaza 'nombre_de_la_vista' con el nombre de tu vista

@login_required
def buscar_usuario(request):
    query = request.GET.get('query')
    if query:
        results = CustomUser.objects.filter(username__icontains=query, is_employee=True)
        data = [{'firstname': result.first_name, 'lastname': result.last_name, 'email': result.username} for result in results]
        return JsonResponse(data, safe=False)
    
    
    return JsonResponse([], safe=False)


@login_required
def agregar_usuario(request):
    if request.method == 'GET':
        project_id = request.GET.get('projectId')
        user_email = request.GET.get('userEmail')
        role_id = request.GET.get('rolUser')
        # Obtener el proyecto
        project = Project.objects.get(id=project_id)

        # Obtener el usuario
        employee = Employee.objects.get(user__email=user_email)
        user_id = CustomUser.objects.get(id=employee.user_id)

        # Obtener el rol
        role = Role.objects.get(id=role_id)

        # Crear la relación entre el proyecto y el usuario con el rol especificado
        ProjectEmployee.objects.create(employee=user_id, project=project, role=role)
        
        # Redirigir a la página de proyectos
        return redirect('proyectos')

    return redirect('proyectos')
