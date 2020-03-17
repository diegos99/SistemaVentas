from django.shortcuts import render
from .formularios import FormularioObjeto, FormularioCliente, FormularioSuscrip
from .models import objeto, cliente, suscripcion
# TIPO DE CLIENTE.
def index(request):
	return render(request, 'ejemplo/index.html')

def formularioAgregarObjeto(request):
	if request.method=="POST":
		formulario = FormularioObjeto(request.POST)
		if formulario.is_valid():
			formulario.save()
	else:
		formulario=FormularioObjeto()
	return render(request, 'clientes/create_tipo_cliente.html', {'formulario':formulario})

def lista_objetos(request):
	objetos = objeto.objects.all()
	return render(request, 'clientes/lista_tipo_cliente.html', {'objetos': objetos})


def editarObjeto(request, objeto_id):
	objetos = objeto.objects.get(id = objeto_id)
	if request.method=="POST":
		formulario = FormularioObjeto(request.POST, instance=objetos)
		if formulario.is_valid():
			formulario.save()
			return render(request, "clientes/create_tipo_cliente.html", {"formulario":formulario})
	else:
		formulario = FormularioObjeto(instance=objetos)
		return render(request, "clientes/create_tipo_cliente.html", {"formulario":formulario})




# CLIENTES
def formularioAgregarCliente(request):
	if request.method=="POST":
		formulario = FormularioCliente(request.POST)
		if formulario.is_valid():
			formulario.save()
	else:
		formulario=FormularioCliente()
	return render(request, 'clientes/create_update_clientes.html', {'formulario':formulario})

def lista_clientes(request):
	clientes = cliente.objects.all()
	return render(request, 'clientes/lista_cliente.html', {'clientes': clientes})

def detalle_clientes(request, cliente_id):
	clientes = cliente.objects.get(id = cliente_id)
	return render(request, 'clientes/detalle_clientes.html', {'clientes': clientes})

def editarCliente(request, cliente_id):
	clientes = cliente.objects.get(id = cliente_id)
	if request.method=="POST":
		formulario = FormularioCliente(request.POST, instance=clientes)
		if formulario.is_valid():
			formulario.save()
			return render(request, "clientes/editar_cliente.html", {"formulario":formulario})
	else:
		formulario = FormularioCliente(instance=clientes)
		return render(request, "clientes/editar_cliente.html", {"formulario":formulario})

def eliminarCliente(request, cliente_id):
	clientes = cliente.objects.get(id = cliente_id)
	clientes.delete()	
	return render(request, 'clientes/eliminar_cliente.html')

# SUSCRIPCIONES
def formularioAgregarSuscrip(request):
	if request.method=="POST":
		formulario = FormularioSuscrip(request.POST)
		if formulario.is_valid():
			formulario.save()
	else:
		formulario=FormularioSuscrip()
	return render(request, 'suscripciones/create_suscrip.html', {'formulario':formulario})

def lista_suscripciones(request):
	suscripciones = suscripcion.objects.all()
	return render(request, 'suscripciones/lista_suscrip.html', {'suscripciones': suscripciones})

def detalle_suscrip(request, suscripcion_id):
	suscripciones = suscripcion.objects.get(id = suscripcion_id)
	return render(request, 'suscripciones/detalle_suscrip.html', {'suscripciones': suscripciones})

def editarSuscripcion(request, suscripcion_id):
	suscripciones = suscripcion.objects.get(id = suscripcion_id)
	if request.method=="POST":
		formulario = FormularioSuscrip(request.POST, instance=suscripciones)
		if formulario.is_valid():
			formulario.save()
			return render(request, "suscripciones/editar_suscrip.html", {"formulario":formulario})
	else:
		formulario = FormularioSuscrip(instance=suscripciones)
		return render(request, "suscripciones/editar_suscrip.html", {"formulario":formulario})

def eliminarSuscripcion(request, suscripcion_id):
	suscripciones = suscripcion.objects.get(id = suscripcion_id)
	suscripciones.delete()	
	return render(request, 'suscripciones/eliminar_suscrip.html')