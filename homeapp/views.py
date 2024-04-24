from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

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
            proyecto = Proyecto(nombre=nombre, descripcion=descripcion, fecha_inicio=fecha_inicio, fecha_final=fecha_final)
            proyecto.constructora = request.user
            proyecto.save()
            return redirect(proyectos_info)
        except:
            return render(request, 'nuevo-proyecto.html', {'error': 'Ingresa datos válidos.'})

@login_required
def proyectos_info(request):
    proyecto_usuarios = ProyectoUsuario.objects.all()
    proyectos = Proyecto.objects.all()
    usuario_actual = request.user
    return render(request, 'proyectos.html', {'proyectos': proyectos, 'usuarios': proyecto_usuarios, 'usuario_actual': usuario_actual})

@login_required
def buscar_usuario(request):
    query = request.GET.get('query')
    if query:
        results = Usuario.objects.filter(username__icontains=query)
        data = [{'firstname': result.first_name, 'lastname': result.last_name, 'email': result.username, 'doc': result.documento} for result in results]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

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