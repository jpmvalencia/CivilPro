from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Proyecto, ProyectoUsuario

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
    return render(request, 'proyectos.html', {'proyectos': proyectos, 'usuarios': proyecto_usuarios})