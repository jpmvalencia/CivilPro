from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate
from django.db import connection

from homeapp.views import proyectos_info
from .models import Usuario, Titulo, UsuarioTitulo#, Constructora

    
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Verificar si el usuario es un Usuario
        user = authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(proyectos_info) 
        # Si no es un Usuario, verificar si es una Constructora
        try:
            constructora = Constructora.objects.get(correo=email)
            if constructora.contraseña == password:
                return redirect(proyectos_info) 
            else:
                return render(request, 'login.html', {'error': 'Correo o contraseña es incorrecto.', 'data': request.POST})
        except Constructora.DoesNotExist:
            return render(request, 'login.html', {'error': 'Correo o contraseña es incorrecto.', 'data': request.POST})

    return render(request, 'login.html')

    

# Create your views here.

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'titulos_disponibles': Titulo.objects.all()})
    else:
        if request.POST['password'] == request.POST['repassword']:
            try:
                user = Usuario.objects.create_user(
                    username=request.POST['your_email'],
                    password=request.POST['password'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['your_email'],
                    documento=request.POST['doc_id'],
                    codigo_pais=request.POST['code'],
                    telefono=request.POST['phone']
                    )
                titulos = request.POST.getlist('titles[]')
                for titulo_nombre in titulos:
                    titulo = Titulo.objects.get(nombre=titulo_nombre)
                    usuario_titulo = UsuarioTitulo.objects.create(
                        id_usuario=user, id_titulo=titulo
                        )
                print(request.POST)
                auth.login(request, user)
                return redirect('../login')
            except:
                return render(request, 'signup.html', {'titulos_disponibles': Titulo.objects.all(), 'error': 'Ya existe un usuario registrado con ese correo.', 'data': request.POST})
        return render(request, 'signup.html', {'titulos_disponibles': Titulo.objects.all(), 'error': 'Las contraseñas no coinciden.', 'data': request.POST})
    

def signupcon(request):
    if request.method == 'GET':
        return render(request, 'signup-con.html')
    else:
        if request.POST['password'] == request.POST['repassword']:
            try:
                with connection.cursor() as cursor:
                    nit_id = request.POST['nit_id']
                    first_name = request.POST['first_name']
                    email = request.POST['your_email']
                    password = request.POST['password']
                    telefono = request.POST['phone']

                    query = """
                        INSERT INTO constructoras (nit_con, nombre_con, correo_con, contraseña_con, telefono_con)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, [nit_id, first_name, email, password, telefono])
                
                user = Usuario.objects.create_user(
                    username=email,
                    password=password,
                    first_name=first_name,
                    email=email,
                    documento=nit_id,
                    codigo_pais=request.POST['code'],
                    telefono=request.POST['phone']
                )

                print(request.POST)
                auth.login(request, user)
                return redirect('../login')
            except Exception as e:
                print(e)  # Log the error
                return render(request, 'signup-con.html', {'error': 'Ya existe un usuario registrado con ese correo.', 'data': request.POST})
        return render(request, 'signup-con.html', {'error': 'Las contraseñas no coinciden.', 'data': request.POST})


@login_required
def signout(request):
    auth.logout(request)
    return redirect('/login')