from django.shortcuts import render
from .formularios import FormularioTipoCliente, FormularioCliente, FormularioSuscrip, FormularioRepuestos, FormularioFabricas, FormularioVehiculos, FormularioCompat
from .models import tipocliente, cliente, suscripcion, repuesto, fabrica, vehiculo, compatibilidad, Factura, DetalleFactura, Orden, DetalleOrden

from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.db import transaction
from django.core import serializers
from django.contrib import messages
from django.views.generic import ListView
from django.template import RequestContext
from django.template import RequestContext as ctx
from django.views.generic import TemplateView
from django.template.loader import get_template
from django.template import Context

from datetime import datetime
import decimal
from django.utils import timezone
import json

# TIPO DE CLIENTE.
def index(request):
    return render(request, 'ejemplo/index.html')


def formularioAgregarTipoCliente(request):
    if request.method == "POST":
        formulario = FormularioTipoCliente(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioTipoCliente()
    return render(request, 'clientes/create_tipo_cliente.html', {'formulario': formulario})


def lista_tipo_clientes(request):
	cursor = connection.cursor()
	cursor.execute("SELECT id, descripcion, descuento FROM ejemplo_tipocliente")
	tipoclientes = cursor.fetchall()
	return render(request, 'clientes/lista_tipo_cliente.html', {'tipoclientes': tipoclientes})
	# tipoclientes = tipocliente.objects.all()
	# return render(request, 'clientes/lista_tipo_cliente.html', {'tipoclientes': tipoclientes})
    

def editarTipoCliente(request, tipo_cliente_id):
    tipoclientes = tipocliente.objects.get(id=tipo_cliente_id)
    if request.method == "POST":
        formulario = FormularioTipoCliente(request.POST, instance=tipoclientes)
        if formulario.is_valid():
            formulario.save()
            return render(request, "clientes/create_tipo_cliente.html", {"formulario": formulario})
    else:
        formulario = FormularioTipoCliente(instance=tipoclientes)
        return render(request, "clientes/create_tipo_cliente.html", {"formulario": formulario})



# CLIENTES
def formularioAgregarCliente(request):
    if request.method == "POST":
        formulario = FormularioCliente(request.POST, request.FILES or None)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioCliente()
    return render(request, 'clientes/create_update_clientes.html', {'formulario': formulario})


def lista_clientes(request):
    clientes = cliente.objects.all()
    return render(request, 'clientes/lista_cliente.html', {'clientes': clientes})


def detalle_clientes(request, cliente_id):
    clientes = cliente.objects.get(id=cliente_id)
    return render(request, 'clientes/detalle_clientes.html', {'clientes': clientes})


def editarCliente(request, cliente_id):
    clientes = cliente.objects.get(id=cliente_id)
    if request.method == "POST":
        formulario = FormularioCliente(
            request.POST, request.FILES, instance=clientes)
        if formulario.is_valid():
            formulario.save()
            return render(request, "clientes/editar_cliente.html", {"formulario": formulario})
    else:
        formulario = FormularioCliente(instance=clientes)
        return render(request, "clientes/editar_cliente.html", {"formulario": formulario})


def eliminarCliente(request, cliente_id):
    clientes = cliente.objects.get(id=cliente_id)
    clientes.delete()
    return render(request, 'clientes/eliminar_cliente.html')


# SUSCRIPCIONES
def formularioAgregarSuscrip(request):
    if request.method == "POST":
        formulario = FormularioSuscrip(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioSuscrip()
    return render(request, 'suscripciones/create_suscrip.html', {'formulario': formulario})


def lista_suscripciones(request):
    suscripciones = suscripcion.objects.all()
    return render(request, 'suscripciones/lista_suscrip.html', {'suscripciones': suscripciones})


def detalle_suscrip(request, suscripcion_id):
    suscripciones = suscripcion.objects.get(id=suscripcion_id)
    return render(request, 'suscripciones/detalle_suscrip.html', {'suscripciones': suscripciones})


def editarSuscripcion(request, suscripcion_id):
    suscripciones = suscripcion.objects.get(id=suscripcion_id)
    if request.method == "POST":
        formulario = FormularioSuscrip(request.POST, instance=suscripciones)
        if formulario.is_valid():
            formulario.save()
            return render(request, "suscripciones/editar_suscrip.html", {"formulario": formulario})
    else:
        formulario = FormularioSuscrip(instance=suscripciones)
        return render(request, "suscripciones/editar_suscrip.html", {"formulario": formulario})


def eliminarSuscripcion(request, suscripcion_id):
    suscripciones = suscripcion.objects.get(id=suscripcion_id)
    suscripciones.delete()
    return render(request, 'suscripciones/eliminar_suscrip.html')


#FABRICAS
def formularioAgregarFabrica(request):
    if request.method == "POST":
        formulario = FormularioFabricas(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioFabricas()
    return render(request, 'fabricas/create_fabricas.html', {'formulario': formulario})

def lista_fabricas(request):
    fabricas = fabrica.objects.all()
    return render(request, 'fabricas/lista_fabricas.html', {'fabricas': fabricas})


def detalle_fabricas(request, fabrica_id):
    fabricas = fabrica.objects.get(id=fabrica_id)
    return render(request, 'fabricas/detalle_fabricas.html', {'fabricas': fabricas})


def editarFabrica(request, fabrica_id):
    fabricas = fabrica.objects.get(id=fabrica_id)
    if request.method == "POST":
        formulario = FormularioFabricas(
            request.POST, instance=fabricas)
        if formulario.is_valid():
            formulario.save()
            return render(request, "fabricas/editar_fabricas.html", {"formulario": formulario})
    else:
        formulario = FormularioFabricas(instance=fabricas)
        return render(request, "fabricas/editar_fabricas.html", {"formulario": formulario})


def eliminarFabrica(request, fabrica_id):
    fabricas = repuesto.objects.get(id=fabrica_id)
    fabricas.delete()
    return render(request, 'fabricas/eliminar_fabricas.html')



#REPUESTOS
def formularioAgregarRepuesto(request):
    if request.method == "POST":
        formulario = FormularioRepuestos(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioRepuestos()
    return render(request, 'repuestos/create_repuestos.html', {'formulario': formulario})

""" def lista_repuestos(request):
    repuestos = repuesto.objects.all()
    return render(request, 'repuestos/lista_repuestos.html', {'repuestos': repuestos}) """
class lista_repuestos(ListView):
	context_object_name = 'repuestos'
	model = repuesto
	template_name = 'repuestos/lista_repuestos.html'


def detalle_repuestos(request, repuesto_id):
    repuestos = repuesto.objects.get(id=repuesto_id)
    return render(request, 'repuestos/detalle_repuestos.html', {'repuestos': repuestos})


def editarRepuesto(request, repuesto_id):
    repuestos = repuesto.objects.get(id=repuesto_id)
    if request.method == "POST":
        formulario = FormularioRepuestos(
            request.POST, request.FILES, instance=repuestos)
        if formulario.is_valid():
            formulario.save()
            return render(request, "repuestos/editar_repuestos.html", {"formulario": formulario})
    else:
        formulario = FormularioRepuestos(instance=repuestos)
        return render(request, "repuestos/editar_repuestos.html", {"formulario": formulario})


def eliminarRepuesto(request, repuesto_id):
    repuestos = repuesto.objects.get(id=repuesto_id)
    repuestos.delete()
    return render(request, 'repuestos/eliminar_repuestos.html')


#VEHICULOS
def formularioAgregarVehiculo(request):
    if request.method == "POST":
        formulario = FormularioVehiculos(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioVehiculos()
    return render(request, 'vehiculos/create_vehiculos.html', {'formulario': formulario})

def lista_vehiculos(request):
    vehiculos = vehiculo.objects.all()
    return render(request, 'vehiculos/lista_vehiculos.html', {'vehiculos': vehiculos})


def detalle_vehiculos(request, vehiculo_id):
    vehiculos = vehiculo.objects.get(id=vehiculo_id)
    return render(request, 'vehiculos/detalle_vehiculos.html', {'vehiculos': vehiculos})


def editarVehiculo(request, vehiculo_id):
    vehiculos = vehiculo.objects.get(id=vehiculo_id)
    if request.method == "POST":
        formulario = FormularioVehiculos(
            request.POST, instance=vehiculos)
        if formulario.is_valid():
            formulario.save()
            return render(request, "vehiculos/editar_vehiculos.html", {"formulario": formulario})
    else:
        formulario = FormularioVehiculos(instance=vehiculos)
        return render(request, "vehiculos/editar_vehiculos.html", {"formulario": formulario})


def eliminarVehiculo(request, vehiculo_id):
    vehiculos = vehiculo.objects.get(id=vehiculo_id)
    vehiculos.delete()
    return render(request, 'vehiculos/eliminar_vehiculos.html')


#COMPATIBILIDAD
def formularioAgregarCompat(request):
    if request.method == "POST":
        formulario = FormularioCompat(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioCompat()
    return render(request, 'compat/create_compat.html', {'formulario': formulario})

def lista_compats(request):
	cursor = connection.cursor()
	cursor.execute("SELECT  ejemplo_compatibilidad.id, ejemplo_repuesto.id, ejemplo_repuesto.nombre, ejemplo_repuesto.descripcion, ejemplo_vehiculo.id, ejemplo_vehiculo.marca, ejemplo_vehiculo.linea, ejemplo_vehiculo.anio FROM ejemplo_compatibilidad INNER JOIN ejemplo_repuesto ON ejemplo_compatibilidad.repuesto_id = ejemplo_repuesto.id INNER JOIN ejemplo_vehiculo ON ejemplo_compatibilidad.vehiculo_id = ejemplo_vehiculo.id;")
	compatibilidades = cursor.fetchall()
	return render(request, 'compat/lista_compat.html', {'compatibilidades': compatibilidades})
	# compatibilidades = compatibilidad.objects.all()
    # return render(request, 'compat/lista_compat.html', {'compatibilidades': compatibilidades})

def detalle_compats(request, compatibilidad_id):
    compatibilidades = compatibilidad.objects.get(id=compatibilidad_id)
    return render(request, 'compat/detalle_compat.html', {'compatibilidades': compatibilidades})


def editarCompat(request, compatibilidad_id):
    compatibilidades = compatibilidad.objects.get(id=compatibilidad_id)
    if request.method == "POST":
        formulario = FormularioCompat(
            request.POST, instance=compatibilidades)
        if formulario.is_valid():
            formulario.save()
            return render(request, "compat/editar_compat.html", {"formulario": formulario})
    else:
        formulario = FormularioCompat(instance=compatibilidades)
        return render(request, "compat/editar_compat.html", {"formulario": formulario})


def eliminarCompat(request, compatibilidad_id):
    compatibilidades = compatibilidad.objects.get(id=compatibilidad_id)
    compatibilidades.delete()
    return render(request, 'compat/eliminar_compat.html')


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

# FACTURA
@transaction.atomic
def facturaCrear(request):

    form = None
    if request.method == 'POST':
        sid = transaction.savepoint()
        try:
            proceso = json.loads(request.POST.get('proceso'))
            print (proceso)
            if 'clienProv' not in proceso:
                msg = 'La Orden no ha sido seleccionado'
                raise Exception(msg)

            if len(proceso['detalleorden']) <= 0:
                msg = 'No se ha seleccionado ningun detalleorden'
                raise Exception(msg)

            

            for k in proceso['detalleorden']:
                detalleorden = DetalleOrden.objects.get(id=k['id'])
                #subTotal = (producto.precio_venta) * int(k['cantidad'])
                #tot = subTotal + ((producto.igv) * int(k['cantidad']))
                #total += tot
            orden=Orden.objects.get(id=proceso['clienProv'])
            crearFactura = Factura(
                orden=orden,
                cliente= orden.cliente,
                fecha= timezone.now(),
                total= orden.total,
            )
            
            crearFactura.save()
            print ("Factura guardado")
            print (crearFactura.id)
            for k in proceso['detalleorden']:
                detalleorden = DetalleOrden.objects.get(id=k['id'])
                crearDetalle = DetalleFactura(
                    detalleorden=detalleorden,
                    producto = detalleorden.producto,
                    descripcion=detalleorden.descripcion,
                    fabrica=detalleorden.fabrica,
                    precio = detalleorden.precio,
                    cantidad=detalleorden.cantidad,
                    impuesto=detalleorden.impuesto,
                    subtotal=detalleorden.subtotal,
                    factura = crearFactura,
                    )
                crearDetalle.save()

            messages.success(
                request, 'La venta se ha realizado satisfactoriamente')

        except (Exception, e):
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.error(request, e)

    return render(request, 'factura/crear_factura.html', {'form': form})

# Busqueda de clientes para factura
def buscarCliente(request):
    idOrden = request.GET['id']
    ordenes = Orden.objects.filter(id__contains=idOrden)
    data = serializers.serialize(
        'json', ordenes, fields=('id', 'cliente', 'fecha', 'total'))
    return HttpResponse(data, content_type='application/json')


# Busqueda de producto para factura
def buscarProducto(request):
    idProducto = request.GET['id']
    producto = DetalleOrden.objects.filter(id__contains=idProducto)
    data = serializers.serialize(
        'json', producto, fields=('id', 'orden', 'producto', 'descripcion', 'fabrica', 'precio', 'cantidad', 'impuesto', 'subtotal'))
    return HttpResponse(data, content_type='application/json')

# Listado de ventas
class ListaVentas(ListView):
    template_name = 'factura/lista_venta.html'
    model = Factura
    def get_context_data(self, **kwargs):
        context = super(ListaVentas, self).get_context_data(**kwargs)
        context['events'] =Factura.objects.all()
        context['compras'] = context['events']
        context['paginate_by']=context['events']
        return context
# Detalle de la factura o de la venta
def reporteventas(request, pk):
    compra = Factura.objects.get(pk=pk)
    repuesto = compra.factura.all()
    hora = datetime.today()

    return render(request, 'factura/reporte_venta.html', locals())


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

# ORDEN DE COMPRA
@transaction.atomic
def ordenCrear(request):

    form = None
    if request.method == 'POST':
        sid = transaction.savepoint()
        try:
            proceso = json.loads(request.POST.get('proceso'))
            print (proceso)
            if 'clienProv' not in proceso:
                msg = 'El cliente no ha sido seleccionado'
                raise Exception(msg)

            if len(proceso['producto']) <= 0:
                msg = 'No se ha seleccionado ningun producto'
                raise Exception(msg)

            total = 0

            if proceso['ctipo'] == 3:
                for k in proceso['producto']:
                    producto = repuesto.objects.get(id=k['id'])
                    subTotal = (producto.precio_venta) * int(k['cantidad'])
                    tot = subTotal + ((producto.igv) * int(k['cantidad']))
                    total += tot
            
                crearOrden = Orden(
                    cliente=cliente.objects.get(id=proceso['clienProv']),
                    fecha=timezone.now(),
                    total=total
                )
                """ vendedores=vendedor.objects.get(id=proceso['vend']),
                    tipos=tipo.objects.get(id=proceso['tip']) """
                crearOrden.save()
                print ("Orden guardado")
                print (crearOrden.id)
                for k in proceso['producto']:
                    producto = repuesto.objects.get(id=k['id'])
                    crearDetalle = DetalleOrden(
                        producto=producto,
                        descripcion=producto.nombre,
                        fabrica = producto.fabrica,
                        precio = producto.precio_venta,
                        cantidad=int(k['cantidad']),
                        impuesto=producto.igv * int(k['cantidad']),
                        subtotal=producto.precio_venta * int(k['cantidad']),
                        orden = crearOrden,
                        )
                    crearDetalle.save()

                messages.success(
                    request, 'La Orden de compra se ha generado satisfactoriamente')

            if proceso['ctipo'] == 1:
                for k in proceso['producto']:
                    producto = repuesto.objects.get(id=k['id'])
                    subTotal = (producto.precio_venta) * int(k['cantidad'])
                    tot = subTotal + ((producto.igv) * int(k['cantidad']))
                    total += tot
            
                crearOrden = Orden(
                    cliente=cliente.objects.get(id=proceso['clienProv']),
                    fecha=timezone.now(),
                    total=total - (total * decimal.Decimal(0.1))
                )
                """ vendedores=vendedor.objects.get(id=proceso['vend']),
                    tipos=tipo.objects.get(id=proceso['tip']) """
                crearOrden.save()
                print ("Orden guardado")
                print (crearOrden.id)
                for k in proceso['producto']:
                    producto = repuesto.objects.get(id=k['id'])
                    crearDetalle = DetalleOrden(
                        producto=producto,
                        descripcion=producto.nombre,
                        fabrica = producto.fabrica,
                        precio = producto.precio_venta,
                        cantidad=int(k['cantidad']),
                        impuesto=producto.igv * int(k['cantidad']),
                        subtotal=producto.precio_venta * int(k['cantidad']),
                        orden = crearOrden,
                        )
                    crearDetalle.save()

                messages.success(
                    request, 'La Orden de compra se ha generado satisfactoriamente')

            if proceso['ctipo'] == 2:
                for k in proceso['producto']:
                    producto = repuesto.objects.get(id=k['id'])
                    subTotal = (producto.precio_venta) * int(k['cantidad'])
                    tot = subTotal + ((producto.igv) * int(k['cantidad']))
                    total += tot
            
                crearOrden = Orden(
                    cliente=cliente.objects.get(id=proceso['clienProv']),
                    fecha=timezone.now(),
                    total=total - (total * decimal.Decimal(0.25))
                )
                """ vendedores=vendedor.objects.get(id=proceso['vend']),
                    tipos=tipo.objects.get(id=proceso['tip']) """
                crearOrden.save()
                print ("Orden guardado")
                print (crearOrden.id)
                for k in proceso['producto']:
                    producto = repuesto.objects.get(id=k['id'])
                    crearDetalle = DetalleOrden(
                        producto=producto,
                        descripcion=producto.nombre,
                        fabrica = producto.fabrica,
                        precio = producto.precio_venta,
                        cantidad=int(k['cantidad']),
                        impuesto=producto.igv * int(k['cantidad']),
                        subtotal=producto.precio_venta * int(k['cantidad']),
                        orden = crearOrden,
                        )
                    crearDetalle.save()

                messages.success(
                    request, 'La Orden de compra se ha generado satisfactoriamente')

        except (Exception, e):
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.error(request, e)

    return render(request, 'orden/crear_factura.html', {'form': form})


# Busqueda de clientes para orden
def buscarClient(request):
    idCliente = request.GET['id']
    clientes = cliente.objects.filter(id__contains=idCliente)
    data = serializers.serialize(
        'json', clientes, fields=('id', 'nombre', 'nit', 'email', 'telefono', 'tipo'))
    return HttpResponse(data, content_type='application/json')


# Busqueda de producto para orden
def buscarProduct(request):
    idProducto = request.GET['id']
    producto = repuesto.objects.filter(id__contains=idProducto)
    data = serializers.serialize(
        'json', producto, fields=('id','nombre', 'descripcion', 'fabrica', 'precio_venta', 'stock', 'igv'))
    return HttpResponse(data, content_type='application/json')

# Lista de Ordenes
class ListaOrdenes(ListView):
    template_name = 'orden/lista_venta.html'
    model = Orden
    def get_context_data(self, **kwargs):
        context = super(ListaOrdenes, self).get_context_data(**kwargs)
        context['events'] =Orden.objects.all()
        context['compras'] = context['events']
        context['paginate_by']=context['events']
        return context

# Detalle Orden
def reporteordenes(request, pk):
    compra = Orden.objects.get(pk=pk)
    repuesto = compra.orden.all()
    hora = datetime.today()

    return render(request, 'orden/reporte_orden.html', locals())

