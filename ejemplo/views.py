from django.shortcuts import render
from .formularios import FormularioObjeto
from .models import objeto
# Create your views here.
def index(request):
	return render(request, 'ejemplo/index.html')

def formularioAgregarObjeto(request):
	if request.method=="POST":
		formulario = FormularioObjeto(request.POST)
		if formulario.is_valid():
			formulario.save()
	else:
		formulario=FormularioObjeto()
	return render(request, 'ejemplo/agregarObjeto.html', {'formulario':formulario})

def lista_objetos(request):
	objetos = objeto.objects.all()
	return render(request, 'ejemplo/listaObjeto.html', {'objetos': objetos})

def editarObjeto(request, objeto_id):
	objetos = objeto.objects.get(id = objeto_id)
	if request.method=="POST":
		formulario = FormularioObjeto(request.POST, instance=objetos)
		if formulario.is_valid():
			formulario.save()
			return render(request, "ejemplo/editarObjeto.html", {"formulario":formulario})
	else:
		formulario = FormularioObjeto(instance=objetos)
		return render(request, "ejemplo/editarObjeto.html", {"formulario":formulario})

def eliminarObjeto(request, objeto_id):
	objetos = objeto.objects.get(id = objeto_id)
	objetos.delete()
	return render(request, '/ejemplo/index.html')
