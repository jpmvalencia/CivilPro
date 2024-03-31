from django.shortcuts import render, redirect
from .models import Usuario, Titulo, UsuarioTitulo

def login(request):
    return render(request, 'login.html')

# Create your views here.
def home(request):
    return render(request, 'home.html')

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
                return redirect('../login')
            except:
                return render(request, 'signup.html', {'titulos_disponibles': Titulo.objects.all(), 'error': 'Ya existe un usuario registrado con ese correo.', 'data': request.POST})
        return render(request, 'signup.html', {'titulos_disponibles': Titulo.objects.all(), 'error': 'Las contraseñas no coinciden.', 'data': request.POST})
    