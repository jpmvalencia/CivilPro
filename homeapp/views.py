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
            id = request.POST.get('id')
            nombre = request.POST.get('title')
            descripcion = request.POST.get('description')
            fecha_inicio = request.POST.get('start-date')
            fecha_final = request.POST.get('end-date')
            presupuesto = request.POST.get('presupuesto')

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Tareas (nombre_tar, descripcion_tar, fecha_inicio_tar, fecha_final_tar, presupuesto_tar) VALUES (%s, %s, %s, %s, %s)",
                    [nombre, descripcion, fecha_inicio, fecha_final, presupuesto]
                )
            
            return redirect('proyectos_info')
            return redirect(proyectos_info)
        except:
            return render(request, 'nueva-tarea.html', {'error': 'Ingresa datos válidos.'})
        
        
@login_required
def nuevo_proyecto(request):
    if request.method == 'GET':
        return render(request, 'nuevo-proyecto.html')
    else:
        try:
            nombre = request.POST.get('title')
            descripcion = request.POST.get('description')
            fecha_inicio = request.POST.get('start-date')
            fecha_final = request.POST.get('end-date')
            presupuesto = request.POST.get('presupuesto')

            print(nombre, descripcion, fecha_inicio, fecha_final, presupuesto)
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Proyectos (id_pro, nombre_pro, descripcion_pro, fecha_inicio_pro, fecha_final_pro, presupuesto_pro, NIT_con_pro) VALUES (proyecto_seq.NEXTVAL, %s, %s, %s, %s, %s, %s)",
                    [nombre, descripcion, fecha_inicio, fecha_final, presupuesto, 4]
                )
            
            return redirect('proyectos_info')  # Ajusta la URL de redirección según sea necesario
        except Exception as e:
            return render(request, 'nuevo-proyecto.html', {'error': 'Ingresa datos válidos.'})


@login_required
def proyectos_info(request):
    usuario_actual = request.user
    
    # Consulta cruda para obtener todos los proyectos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM proyectos")
        proyectos_raw = cursor.fetchall()

    # Convertir los datos de proyectos a una lista de diccionarios
    proyectos = []
    for row in proyectos_raw:
        proyectos.append({'id': row[0], 'nombre': row[1], 'descripcion': row[2], 'fecha_inicio': row[3], 'fecha_final': row[4], 'presupuesto': row[5], 'constructora_id': row[6]})
    
    # Consulta cruda para obtener todos los usuarios relacionados con proyectos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM miembros_proyectos")
        proyecto_usuarios_raw = cursor.fetchall()
    
    # NO FUNCIONA
    # Convertir los datos de proyecto_usuarios a una lista de diccionarios
    proyecto_usuarios = []
    for row in proyecto_usuarios_raw:
        proyecto_usuarios.append({'documento_mie_pro': row[0], 'id_pro_mie': row[1], 'nombre_rol_mie_pro': row[2], 'nit_con_mie_pro': row[3]})


    # Obtener los roles desde la base de datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM roles1")
        roles_raw = cursor.fetchall()  # Esto me da una lista de tuplas
        
    roles = [row[0] for row in roles_raw]


    # Obtener las tareas desde la base de datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Tareas")
        tareas_row = cursor.fetchall()  # Esto te da una lista de tuplas
    
    # Convertir los datos de tareas_row a una lista de diccionarios
    tareas = []
    for row in tareas_row:
        tareas.append({
            'id_tar': row[0],
            'nombre_tar': row[1],
            'descripcion_tar': row[2],
            'fecha_inicio_tar': row[3],
            'fecha_final_tar': row[4],
            'presupuesto_tar': row[5],
            'responsable_tar': row[6],
            'id_pro_tar': row[7]
        })
    print("---------------")
    print(tareas)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 1 
            FROM constructoras 
            WHERE nit_con = %s
        """, [usuario_actual.documento])
        show_link = cursor.fetchone() is not None  

    return render(request, 'proyectos.html', {'proyectos': proyectos, 'usuarios': proyecto_usuarios, 'usuario_actual': usuario_actual,'tareas' : tareas , 'roles': roles,'show_link': show_link})



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
        rolUser = request.GET.get('rolUser')
        
        print("---------------------------------------------")
        print(userEmail)
        print("---------------------------------------------")
        print(projectId)
        print("---------------------------------------------")
        print(rolUser)
        print("---------------------------------------------")

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM roles1 WHERE nombre_rol = %s", [rolUser])
            rol_row = cursor.fetchone()
            print(rol_row)
            cursor.execute("SELECT id FROM authentapp_usuario WHERE email = %s", [userEmail])
            user_row = cursor.fetchone()
            print(user_row)
            cursor.execute("SELECT id_pro FROM proyectos WHERE id_pro = %s", [projectId])
            proyecto_row = cursor.fetchone()
            print(proyecto_row)

            
        # Obtener los IDs correspondientes
        rolUser_id = rol_row[0]
        user_id = user_row[0]
        proyecto_id = proyecto_row[0]
        print("Llega hasta aquí")
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO miembros_proyectos (documento_mie_pro, id_pro_mie, nombre_rol_mie_pro, nit_con_mie_pro) VALUES (%s, %s, %s, %s)",
            [user_id, proyecto_id, rolUser_id, 'j']
        )# Realizar la inserciónwith connection.cursor() as cursor:
    


    return redirect('/proyectos')
