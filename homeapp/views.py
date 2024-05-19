from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection


from .models import Usuario
from .models import Proyecto, ProyectoUsuario
from authentapp.models import Usuario

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def nuevo_proyecto(request):
    if request.method == 'GET':
        return render(request, 'nuevo-proyecto.html')
    else:
        try:
            print(request.POST)
            nombre = request.POST.get('title')
            descripcion = request.POST.get('description')
            fecha_inicio = request.POST.get('start-date')
            fecha_final = request.POST.get('end-date')
            presupuesto = request.POST.get('presupuesto')
            proyecto = Proyecto(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio, fecha_final=fecha_final, presupuesto=presupuesto)
            proyecto.constructora = request.user
            proyecto.save()
            return redirect(proyectos_info)
        except:
            return render(request, 'nuevo-proyecto.html', {'error': 'Ingresa datos válidos.'})

@login_required
def proyectos_info(request):
    usuario_actual = request.user

    # Consulta cruda para obtener todos los proyectos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM homeapp_proyecto")
        proyectos_raw = cursor.fetchall()
    
    # Convertir los datos de proyectos a una lista de diccionarios
    proyectos = []
    for row in proyectos_raw:
        proyectos.append({'id': row[0], 'nombre': row[1], 'descripcion': row[2], 'estado': row[3], 'fecha_inicio': row[4], 'fecha_final': row[5], 'presupuesto': row[6], 'constructora_id': row[7]})

    # Consulta cruda para obtener todos los usuarios relacionados con proyectos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM homeapp_proyectousuario")
        proyecto_usuarios_raw = cursor.fetchall()
    
    # NO FUNCIONA
    # Convertir los datos de proyecto_usuarios a una lista de diccionarios
    proyecto_usuarios = []
    for row in proyecto_usuarios_raw:
        proyecto_usuarios.append({'id': row[0], 'id_proyecto': row[1], 'id_usuario': row[2]})

    return render(request, 'proyectos.html', {'proyectos': proyectos, 'usuarios': proyecto_usuarios, 'usuario_actual': usuario_actual})

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

        # Obtener el usuario por email usando una consulta SQL cruda
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM authentapp_usuario WHERE email = %s", [userEmail])
            user_row = cursor.fetchone()

        user_id = user_row[0]

        # Verificar si el proyecto existe usando una consulta SQL cruda
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM homeapp_proyecto WHERE id = %s", [projectId])
            proyecto_row = cursor.fetchone()

        proyecto_id = proyecto_row[0]

        # Crear una nueva entrada en ProyectoUsuario usando una consulta SQL cruda
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO homeapp_proyectousuario (id_usuario_id, id_proyecto_id) VALUES (%s, %s)",
                [user_id, proyecto_id]
            )
    return redirect(proyectos_info)