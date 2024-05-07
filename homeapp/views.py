from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db import connection
from .models import Usuario
from .models import Proyecto, ProyectoUsuario, Tarea
from authentapp.models import Usuario

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def nueva_tarea(request):
    if request.method == 'GET':
        return render(request,'nueva-tarea.html')
    else:
        try:
            print(request.POST)
            nombre = request.POST.get('title')
            descripcion = request.POST.get('description')
            fecha_inicio = request.POST.get('start-date')
            fecha_final = request.POST.get('end-date')
            presupuesto = request.POST.get('presupuesto')
            tarea = Tarea(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio, fecha_final=fecha_final, presupuesto=presupuesto)
            
            tarea.save()
            return redirect(proyectos_info)
        except:
            return render(request, 'nueva-tarea.html', {'error': 'Ingresa datos válidos.'})
        


@login_required
def nuevo_proyecto(request):
    if request.method == 'GET':
        return render(request, 'nuevo-proyecto.html')
    else:
        try:
            print(request.POST)
            nombre = request.POST.get('title')
            descripcion = request.POST.get('description')
            estado = 'En progreso'  # Estado predeterminado
            fecha_inicio = request.POST.get('start-date')
            fecha_final = request.POST.get('end-date')
            presupuesto = request.POST.get('presupuesto')
            with connection.cursor() as cursor:
                # Ejecutar consulta SQL para insertar un nuevo proyecto
                cursor.execute(
                    """
                    INSERT INTO homeapp_proyecto
                    (nombre, descripcion, estado, fecha_inicio, fecha_final, constructora_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    [nombre, descripcion, estado, fecha_inicio, fecha_final, request.user.id]
                )
            return redirect(proyectos_info)
        except Exception as e:
            print(e)
            return render(request, 'nuevo-proyecto.html', {'error': 'Ingresa datos válidos.'})
        
@login_required
def proyectos_info(request):
    proyecto_usuarios = ProyectoUsuario.objects.all()
    proyectos = Proyecto.objects.all()
    usuario_actual = request.user
    tareas = Tarea.objects.all()
    return render(request, 'proyectos.html', {'proyectos': proyectos, 'tareas': tareas, 'usuarios': proyecto_usuarios, 'usuario_actual': usuario_actual})


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
        results = Usuario.objects.filter(username__icontains=query)
        data = [{'firstname': result.first_name, 'lastname': result.last_name, 'email': result.username, 'doc': result.documento} for result in results]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

@login_required
def agregar_usuario(request):
    if request.method == 'GET':
        projectId = request.GET.get('projectId')
        userEmail = request.GET.get('userEmail')

        # Assuming Usuario and ProyectoUsuario models are correctly imported
        user = Usuario.objects.get(email=userEmail)
        proyecto = Proyecto.objects.get(id=projectId)

        # Create ProyectoUsuario instance
        proyecto_usuario = ProyectoUsuario.objects.create(id_usuario=user, id_proyecto=proyecto)
        proyecto_usuario.save()

        # Handle response if needed
    return redirect(proyectos_info)
