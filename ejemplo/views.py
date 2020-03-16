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
	return render(request, 'clientes/create_update_clientes.html', {'formulario':formulario})

def lista_objetos(request):
	objetos = objeto.objects.all()
	return render(request, 'clientes/lista_cliente.html', {'objetos': objetos})

def detalle_objetos(request, objeto_id):
	objetos = objeto.objects.get(id = objeto_id)
	return render(request, 'clientes/detalle_clientes.html', {'objetos': objetos})

def editarObjeto(request, objeto_id):
	objetos = objeto.objects.get(id = objeto_id)
	if request.method=="POST":
		formulario = FormularioObjeto(request.POST, instance=objetos)
		if formulario.is_valid():
			formulario.save()
			return render(request, "clientes/editar_cliente.html", {"formulario":formulario})
	else:
		formulario = FormularioObjeto(instance=objetos)
		return render(request, "clientes/editar_cliente.html", {"formulario":formulario})

def eliminarObjeto(request, objeto_id):
	objetos = objeto.objects.get(id = objeto_id)
	objetos.delete()	
	return render(request, 'clientes/eliminar_cliente.html')
	messages.success(
                request, 'La venta se ha realizado satisfactoriamente')
