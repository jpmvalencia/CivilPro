from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import connection
from .models import Employee, Role#Usuario
from .models import Project, ProjectEmployee, Task, ProjectEmployee #Proyecto, ProyectoUsuario, Tarea
from authentapp.models import Employee, CustomUser

# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def nueva_tarea(request, id_proyecto):
    if request.method == 'GET':
        return render(request,'nueva-tarea.html')
    else:
        try:
            nombre = request.POST.get('title')
            descripcion = request.POST.get('description')
            fecha_inicio = request.POST.get('start-date')
            fecha_final = request.POST.get('end-date')
            presupuesto = request.POST.get('presupuesto')
            print(nombre, descripcion, fecha_inicio, fecha_final, presupuesto, id_proyecto)
            with connection.cursor() as cursor:
                cursor.execute("SELECT MAX(ID_TAR) FROM TAREAS")
                max_id = cursor.fetchone()[0]
                id_tareas = 1 if max_id is None else max_id + 1
                cursor.execute(
                    "INSERT INTO Tareas (id_tar, nombre_tar, descripcion_tar, fecha_inicio_tar, fecha_final_tar, presupuesto_tar, id_pro_tar) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    [id_tareas, nombre, descripcion, fecha_inicio, fecha_final, presupuesto, id_proyecto]
                )
            
            return redirect('proyectos')
        except:
            return render(request, 'nueva-tarea.html', {'error': 'Ingresa datos válidos.'})
        
        
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Project

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
            print("El guardado se ha realizado con éxito.")
            return redirect('proyectos')  # Redirige a la página de proyectos
        except Exception as e:
            # Mostrar mensaje de error en caso de fallo
            print(f"Error al guardar el proyecto: {e}")
            return render(request, 'nuevo-proyecto.html', {'error': 'Ingresa datos válidos.'})

        
@login_required
def eliminar_proyecto(request, id_proyecto):
    try:
        proyecto = Project.objects.get(id=id_proyecto)
        proyecto.delete()
        return redirect('proyectos')
    except Project.DoesNotExist:
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
            print("El guardado se ha realizado con éxito.")
            return redirect('proyectos')  # Redirige a la página de proyectos
        except Exception as e:
            # Mostrar mensaje de error en caso de fallo
            print(f"Error al guardar el proyecto: {e}")
            return render(request, 'nuevo-proyecto.html', {'error': 'Ingresa datos válidos.'})

@login_required
def proyectos_info(request):
    # usuario_actual = request.user
    
    # with connection.cursor() as cursor:
    #     cursor.execute("""
    #         SELECT 1 
    #         FROM constructoras 
    #         WHERE nit_con = %s
    #     """, [usuario_actual.documento])
    #     show_link = cursor.fetchone() is not None  
    
    # print(show_link)
    #     # cursor.execute("SELECT proyectos.id_pro, tareas.* FROM proyectos INNER JOIN tareas ON tareas.id_pro_tar = proyectos.id_pro")
    # if (show_link == False):

    #     # Consulta cruda para obtener todos los proyectos
    #     with connection.cursor() as cursor:
    #         cursor.execute("""SELECT *
    #                         FROM proyectos 
    #                         WHERE id_pro IN (
    #                             SELECT Id_pro_mie 
    #                             FROM miembros_proyectos 
    #                             WHERE documento_mie_pro = %s)
    #                         """, [usuario_actual.id])
    #         proyecto_raw = cursor.fetchall()
        
    #     # Convertir los datos de proyectos a una lista de diccionarios
    #     proyectos = []
    #     for row in proyecto_raw:
    #         proyectos.append({'id': row[0], 'nombre': row[1], 'descripcion': row[2], 'fecha_inicio': row[3], 'fecha_final': row[4], 'presupuesto': row[5], 'constructora_id': row[6]})
    # else:
    #     # Consulta cruda para obtener todos los proyectos
    #     with connection.cursor() as cursor:
    #         cursor.execute("""SELECT *
    #                         FROM proyectos 
    #                         WHERE nit_con_pro IN (
    #                             SELECT nit_con 
    #                             FROM constructoras
    #                             WHERE nit_con = %s)
    #                         """, [usuario_actual.documento])
    #         proyecto_raw = cursor.fetchall()

    #     print(usuario_actual.documento)
            
    #     # Convertir los datos de proyectos a una lista de diccionarios
    #     proyectos = []
    #     for row in proyecto_raw:
    #         proyectos.append({'id': row[0], 'nombre': row[1], 'descripcion': row[2], 'fecha_inicio': row[3], 'fecha_final': row[4], 'presupuesto': row[5], 'constructora_id': row[6]})
        
    # print(proyectos)

    # # Consulta cruda para obtener todos los usuarios relacionados con proyectos
    # with connection.cursor() as cursor:
    #     cursor.execute("""SELECT miembros_proyectos.*, 
    #                    authentapp_usuario.nombre_usu
    #                     FROM miembros_proyectos
    #                     INNER JOIN authentapp_usuario 
    #                    ON miembros_proyectos.Documento_mie_pro = authentapp_usuario.id""")
    #     proyecto_usuarios_raw = cursor.fetchall()
    
    # # NO FUNCIONA
    # # Convertir los datos de proyecto_usuarios a una lista de diccionarios
    # proyecto_usuarios = []
    # for row in proyecto_usuarios_raw:
    #     proyecto_usuarios.append({'documento_mie_pro': row[0], 'id_pro_mie': row[1], 'nombre_rol_mie_pro': row[2], 'nit_con_mie_pro': row[3], 'nombre': row[4]})

    # print(proyecto_usuarios)

    # # Obtener los roles desde la base de datos
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM roles1")
    #     roles_raw = cursor.fetchall()  # Esto me da una lista de tuplas
        
    # roles = [row[0] for row in roles_raw]
    

    # # Obtener las tareas desde la base de datos
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM Tareas")
    #     tareas_row = cursor.fetchall()  # Esto te da una lista de tuplas
    
    # # Convertir los datos de tareas_row a una lista de diccionarios
    # tareas = []
    # for row in tareas_row:
    #     tareas.append({
    #         'id_tar': row[0],
    #         'nombre_tar': row[1],
    #         'descripcion_tar': row[2],
    #         'fecha_inicio_tar': row[3],
    #         'fecha_final_tar': row[4],
    #         'presupuesto_tar': row[5],
    #         'responsable_tar': row[6],
    #         'id_pro_tar': row[7]
    #     })


    allproyectos = Project.objects.all()
    usuario_actual = request.user
    tareas = Task.objects.all()
    roles = Role.objects.all()
    show_link = False

    if (usuario_actual.is_employee):
        try:
            employee = usuario_actual.employee
            proyectos = Project.objects.filter(projectemployee__employee=employee)
        except Employee.DoesNotExist:
            # Manejo del caso en el que no exista un Employee asociado al usuario
            proyectos = []
    else:
        show_link = True
        try:
            company = usuario_actual.company
            proyectos = Project.objects.filter(company=company)
        except Employee.DoesNotExist:
            # Manejo del caso en el que no exista un Employee asociado al usuario
            proyectos = []

    return render(request, 'proyectos.html', {'proyectos': proyectos, 'usuario_actual': usuario_actual,'tareas' : tareas , 'roles': roles,'show_link': show_link})

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
    print(query)
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
        print(project_id, user_email, role_id)

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
        return redirect('/proyectos')



    return redirect('/proyectos')