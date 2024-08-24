from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate
from django.db import connection

from homeapp.views import proyectos_info
from .models import Company, Employee, Degree, EmployeeDegree#Constructora, Usuario, Titulo, UsuarioTitulo#, Constructora

    
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # user = auth.authenticate(request, username=request.POST['email'], password=request.POST['password'])
        # if user is None:
        #     return render(request, 'login.html', {'error': 'El usuario o contraseña es incorrecto.', 'data': request.POST})
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(proyectos_info)  # Redirigir a la página principal
        auth.login(request, user)
        return redirect(proyectos_info)

    

# Create your views here.

def signup_usu(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'titulos_disponibles': Titulo.objects.all()})
    else:
        if request.POST['password'] == request.POST['repassword']:
            try:
                # user = Usuario.objects.create_user(
                #     username=request.POST['your_email'],
                #     password=request.POST['password'],
                #     first_name=request.POST['first_name'],
                #     last_name=request.POST['last_name'],
                #     email=request.POST['your_email'],
                #     documento=request.POST['doc_id'],
                #     codigo_pais=request.POST['code'],
                #     telefono=request.POST['phone']
                #     )
                # titulos = request.POST.getlist('titles[]')
                # for titulo_nombre in titulos:
                #     titulo = Titulo.objects.get(nombre=titulo_nombre)
                #     usuario_titulo = UsuarioTitulo.objects.create(
                #         id_usuario=user, id_titulo=titulo
                #         )

                # Obtener los datos del formulario
                username = request.POST['your_email']
                password = request.POST['password']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['your_email']
                documento = request.POST['doc_id']
                codigo_pais = request.POST['code']
                telefono = request.POST['phone']
                print("1")

                # Crear una instancia de Usuario y establecer los atributos
                usuario = Usuario(
                    username=username,
                    nombre_usu=first_name,
                    apellido_usu=last_name,
                    correo_usu=email,
                    documento_usu=documento,
                    codigo_pais=codigo_pais,
                    telefono_usu=telefono
                )
                
                print("2")
                usuario.set_password(password)  # Hashear la contraseña
                usuario.save()  # Guardar el usuario en la base de datos
                

                # Asociar títulos al usuario
                titulos = request.POST.getlist('titles[]')
                for titulo_nombre in titulos:
                    titulo = Titulo.objects.get(nombre=titulo_nombre)
                    UsuarioTitulo.objects.create(
                        id_usuario=usuario,
                        id_titulo=titulo
                    )
                print(request.POST)

                # auth.login(request, user)
                return redirect('../login')
            except:
                return render(request, 'signup.html', {'titulos_disponibles': Titulo.objects.all(), 'error': 'Ya existe un usuario registrado con ese correo.', 'data': request.POST})
        return render(request, 'signup.html', {'titulos_disponibles': Titulo.objects.all(), 'error': 'Las contraseñas no coinciden.', 'data': request.POST})
    

def signup_con(request):
    if request.method == 'GET':
        return render(request, 'signup-con.html')
    else:
        if request.POST['password'] == request.POST['repassword']:
            try:
                # with connection.cursor() as cursor:
                #     nit_id = request.POST['nit_id']
                #     first_name = request.POST['first_name']
                #     email = request.POST['your_email']
                #     password = request.POST['password']
                #     telefono = request.POST['phone']

                #     query = """
                #         INSERT INTO constructoras (nit_con, nombre_con, correo_con, contraseña_con, telefono_con)
                #         VALUES (%s, %s, %s, %s, %s)
                #     """
                #     cursor.execute(query, [nit_id, first_name, email, password, telefono])
                
                # user = Usuario.objects.create_user(
                #     username=email,
                #     password=password,
                #     first_name=first_name,
                #     email=email,
                #     documento=nit_id,
                #     codigo_pais=request.POST['code'],
                #     telefono=request.POST['phone']
                # )

                # print(request.POST)
                # auth.login(request, user)

                # Obtener los datos del formulario
                
                username = request.POST['your_email']
                nit_id = request.POST['nit_id']
                first_name = request.POST['first_name']
                email = request.POST['your_email']
                password = request.POST['password']
                telefono = request.POST['phone']

                # Crear una instancia de Constructora y establecer los atributos
                constructora = Constructora(
                    username=username,
                    nit_con=nit_id,
                    nombre_con=first_name,
                    correo_con=email,
                    telefono_con=telefono,
                )
                constructora.set_password(password)  # Hashear la contraseña
                constructora.save()  # Guardar la constructora en la base de datos

                return redirect('../login')
            except Exception as e:
                print(e)  # Log the error
                return render(request, 'signup-con.html', {'error': 'Ya existe un usuario registrado con ese correo.', 'data': request.POST})
        return render(request, 'signup-con.html', {'error': 'Las contraseñas no coinciden.', 'data': request.POST})


@login_required
def signout(request):
    auth.logout(request)
    return redirect('/login')