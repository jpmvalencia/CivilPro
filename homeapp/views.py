from django.shortcuts import redirect, render

from .models import Proyecto
from authentapp.models import Usuario

# Create your views here.
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
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
            return redirect(home)
        except:
            return render(request, 'home.html', {'error': 'Ingresa datos válidos.'})

def proyectos_info(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos-info.html', {'proyectos': proyectos})
def perfil_usuario(request):
    usuario_actual = request.user
    
    return render(request, 'perfil-usuario.html', {'usuario_actual': usuario_actual})