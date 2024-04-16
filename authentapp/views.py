from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from homeapp.views import proyectos_info
from .models import Usuario, Titulo, UsuarioTitulo

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = auth.authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'error': 'El usuario o contraseña es incorrecto.', 'data': request.POST})
        auth.login(request, user)
        return redirect(proyectos_info)

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

@login_required
def signout(request):
    auth.logout(request)
    return redirect('/login')