from django.conf import settings
from django.shortcuts import render, redirect
from .formularios import FormularioTipoCliente, FormularioCliente, FormularioSuscrip, FormularioRepuestos, FormularioFabricas, FormularioVehiculos, FormularioCompat, CreateUserForm, Formu, Formu2
from .models import tipocliente, cliente, suscripcion, repuesto, fabrica, vehiculo, compatibilidad, Factura, DetalleFactura, Orden, DetalleOrden, PedidoRecibido
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.db import transaction
from django.core import serializers
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
import requests

# INDEX Y LOGIN Y REGISTER
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='vendedor')
            user.groups.add(group)

            messages.success(request, 'Account was creater for' + username)

            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def index(request):
    return render(request, 'ejemplo/index.html')

# TIPO DE CLIENTE.
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def formularioAgregarTipoCliente(request):
    if request.method == "POST":
        formulario = FormularioTipoCliente(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioTipoCliente()
    return render(request, 'clientes/create_tipo_cliente.html', {'formulario': formulario})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def lista_tipo_clientes(request):
	cursor = connection.cursor()
	cursor.execute("SELECT id, descripcion, descuento FROM ejemplo_tipocliente")
	tipoclientes = cursor.fetchall()
	return render(request, 'clientes/lista_tipo_cliente.html', {'tipoclientes': tipoclientes})
	# tipoclientes = tipocliente.objects.all()
	# return render(request, 'clientes/lista_tipo_cliente.html', {'tipoclientes': tipoclientes})
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def formularioAgregarCliente(request):
    if request.method == "POST":
        formulario = FormularioCliente(request.POST, request.FILES or None)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioCliente()
    return render(request, 'clientes/create_update_clientes.html', {'formulario': formulario})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def lista_clientes(request):
    clientes = cliente.objects.all()
    return render(request, 'clientes/lista_cliente.html', {'clientes': clientes})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def detalle_clientes(request, cliente_id):
    clientes = cliente.objects.get(id=cliente_id)
    return render(request, 'clientes/detalle_clientes.html', {'clientes': clientes})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def eliminarCliente(request, cliente_id):
    clientes = cliente.objects.get(id=cliente_id)
    clientes.delete()
    return render(request, 'clientes/eliminar_cliente.html')


# SUSCRIPCIONES
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def formularioAgregarSuscrip(request):
    if request.method == "POST":
        formulario = FormularioSuscrip(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioSuscrip()
    return render(request, 'suscripciones/create_suscrip.html', {'formulario': formulario})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def lista_suscripciones(request):
    suscripciones = suscripcion.objects.all()
    return render(request, 'suscripciones/lista_suscrip.html', {'suscripciones': suscripciones})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def detalle_suscrip(request, suscripcion_id):
    suscripciones = suscripcion.objects.get(id=suscripcion_id)
    return render(request, 'suscripciones/detalle_suscrip.html', {'suscripciones': suscripciones})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def eliminarSuscripcion(request, suscripcion_id):
    suscripciones = suscripcion.objects.get(id=suscripcion_id)
    suscripciones.delete()
    return render(request, 'suscripciones/eliminar_suscrip.html')


#FABRICAS
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def formularioAgregarFabrica(request):
    if request.method == "POST":
        formulario = FormularioFabricas(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioFabricas()
    return render(request, 'fabricas/create_fabricas.html', {'formulario': formulario})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def lista_fabricas(request):
    fabricas = fabrica.objects.all()
    return render(request, 'fabricas/lista_fabricas.html', {'fabricas': fabricas})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def detalle_fabricas(request, fabrica_id):
    fabricas = fabrica.objects.get(id=fabrica_id)
    return render(request, 'fabricas/detalle_fabricas.html', {'fabricas': fabricas})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def eliminarFabrica(request, fabrica_id):
    fabricas = repuesto.objects.get(id=fabrica_id)
    fabricas.delete()
    return render(request, 'fabricas/eliminar_fabricas.html')

#REPUESTOS
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def formularioAgregarRepuesto(request):
    if request.method == "POST":
        formulario = FormularioRepuestos(request.POST, request.FILES or None)
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def detalle_repuestos(request, repuesto_id):
    repuestos = repuesto.objects.get(id=repuesto_id)
    return render(request, 'repuestos/detalle_repuestos.html', {'repuestos': repuestos})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def eliminarRepuesto(request, repuesto_id):
    repuestos = repuesto.objects.get(id=repuesto_id)
    repuestos.delete()
    return render(request, 'repuestos/eliminar_repuestos.html')


#VEHICULOS
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def formularioAgregarVehiculo(request):
    if request.method == "POST":
        formulario = FormularioVehiculos(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioVehiculos()
    return render(request, 'vehiculos/create_vehiculos.html', {'formulario': formulario})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def lista_vehiculos(request):
    vehiculos = vehiculo.objects.all()
    return render(request, 'vehiculos/lista_vehiculos.html', {'vehiculos': vehiculos})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def detalle_vehiculos(request, vehiculo_id):
    vehiculos = vehiculo.objects.get(id=vehiculo_id)
    return render(request, 'vehiculos/detalle_vehiculos.html', {'vehiculos': vehiculos})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def eliminarVehiculo(request, vehiculo_id):
    vehiculos = vehiculo.objects.get(id=vehiculo_id)
    vehiculos.delete()
    return render(request, 'vehiculos/eliminar_vehiculos.html')


#COMPATIBILIDAD
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def formularioAgregarCompat(request):
    if request.method == "POST":
        formulario = FormularioCompat(request.POST)
        if formulario.is_valid():
            formulario.save()
    else:
        formulario = FormularioCompat()
    return render(request, 'compat/create_compat.html', {'formulario': formulario})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def lista_compats(request):
	cursor = connection.cursor()
	cursor.execute("SELECT  ejemplo_compatibilidad.id, ejemplo_repuesto.id, ejemplo_repuesto.nombre, ejemplo_repuesto.descripcion, ejemplo_vehiculo.id, ejemplo_vehiculo.marca, ejemplo_vehiculo.linea, ejemplo_vehiculo.anio FROM ejemplo_compatibilidad INNER JOIN ejemplo_repuesto ON ejemplo_compatibilidad.repuesto_id = ejemplo_repuesto.id INNER JOIN ejemplo_vehiculo ON ejemplo_compatibilidad.vehiculo_id = ejemplo_vehiculo.id;")
	compatibilidades = cursor.fetchall()
	return render(request, 'compat/lista_compat.html', {'compatibilidades': compatibilidades})
	# compatibilidades = compatibilidad.objects.all()
    # return render(request, 'compat/lista_compat.html', {'compatibilidades': compatibilidades})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def detalle_compats(request, compatibilidad_id):
    compatibilidades = compatibilidad.objects.get(id=compatibilidad_id)
    return render(request, 'compat/detalle_compat.html', {'compatibilidades': compatibilidades})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def eliminarCompat(request, compatibilidad_id):
    compatibilidades = compatibilidad.objects.get(id=compatibilidad_id)
    compatibilidades.delete()
    return render(request, 'compat/eliminar_compat.html')


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

# FACTURA
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def buscarCliente(request):
    idOrden = request.GET['id']
    ordenes = Orden.objects.filter(id__contains=idOrden)
    data = serializers.serialize(
        'json', ordenes, fields=('id', 'cliente', 'fecha', 'total'))
    return HttpResponse(data, content_type='application/json')


# Busqueda de producto para factura
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
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

# LISTADO DE VENTAS PARA API
def buscarDetalleFacturas(request):
    idFactura = request.GET['id']
    facturas = DetalleFactura.objects.filter(id__contains=idFactura)
    data = serializers.serialize(
        'json', facturas, fields=('id', 'factura', 'detalleorden', 'producto', 'descripcion', 'fabrica', 'precio', 'cantidad', 'impuesto', 'subtotal'))
    return HttpResponse(data, content_type='application/json')
    
# CORREO
def send_email(mail, compra, repuesto, hora):
    template = get_template('factura/reporte_venta.html')
    content = template.render({'compra': compra, 'repuesto': repuesto, 'hora': hora})

    email = EmailMultiAlternatives(
        'Recordatorio de pago',
        ' ',
        settings.EMAIL_HOST_USER,
        [mail]
    )

    email.attach_alternative(content, 'text/html')
    email.send()

# Detalle de la factura o de la venta
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def reporteventas(request, pk):
    compra = Factura.objects.get(pk=pk)
    repuesto = compra.factura.all()
    hora = datetime.today()
    if request.method == 'POST':
        mail = request.POST.get('mail')
        send_email(mail, compra, repuesto, hora)

    return render(request, 'factura/reporte_venta.html', locals())


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

# ORDEN DE COMPRA
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def buscarClient(request):
    idCliente = request.GET['id']
    clientes = cliente.objects.filter(id__contains=idCliente)
    data = serializers.serialize(
        'json', clientes, fields=('id', 'nombre', 'nit', 'email', 'telefono', 'tipo'))
    return HttpResponse(data, content_type='application/json')


# Busqueda de producto para orden
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def buscarProduct(request):
    idProducto = request.GET['id']
    producto = repuesto.objects.filter(id__contains=idProducto)
    data = serializers.serialize(
        'json', producto, fields=('id','nombre', 'descripcion', 'fabrica', 'precio_venta', 'stock', 'igv', 'imagen', 'imagen2'))
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
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def reporteordenes(request, pk):
    compra = Orden.objects.get(pk=pk)
    repuesto = compra.orden.all()
    hora = datetime.today()

    return render(request, 'orden/reporte_orden.html', locals())


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------

# PEDIDOS
@login_required(login_url='login')
def listaCompra(request):
    response = requests.get('http://localhost:8080/api/v1/pedido')
    fabrica = response.json()
    print(fabrica)
    return render(request, 'compras/lista_compras.html', {
        'fabrica': fabrica
        #'data': fabrica[1],
    })


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'vendedor'])
def compra(request):
    if request.method == 'POST':
        payload = {'id': '4', 'fechaEnvio': '20/04/2020', 'producto': 'prod1', 'descripcion': 'gfdgd', 'cantidad': '30'}
        form = Formu(request.POST)
        r = requests.post('http://localhost:8080/api/v1/pedido', json=request.POST)
        pastebin_url = r.text
        print(pastebin_url)
        print(r.status_code)
        print(request.POST)
        print(form)
    else:
        form = Formu()

    return render(request, 'compras/crear_compras.html', {'form': form})

#@login_required(login_url='login')
#def buzon(request):
#    if request.method == "POST":
#        formulario = Formu2(request.POST)
#        if formulario.is_valid():
#            formulario.save()
#    else:
#        formulario = Formu2()
#    return render(request, 'compras/reportecompras.html', {'formulario': formulario})


def lista_recibidos(request):
    recibidos = PedidoRecibido.objects.all()
    return render(request, 'compras/reportecompras.html', {'recibidos': recibidos})

def listaRecibidos(request):
    idRecibido = request.GET['id']
    pedido = PedidoRecibido.objects.filter(id__contains=idRecibido)
    data = serializers.serialize(
        'json', pedido, fields=('id','producto', 'descripcion', 'cantidad'))
    return HttpResponse(data, content_type='application/json')

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin', 'vendedor'])
#def compra(request):
#    payload = {'id': '3', 'fechaEnvio': '20/04/2020', 'producto': 'prod1', 'descripcion': 'gfdgd', 'cantidad': '30'}
#    r = requests.post('http://localhost:8080/api/v1/pedido', json=payload)
#    pastebin_url = r.text
#    print(pastebin_url)
#    print(r.text)
#    print(r.status_code)
#    return render(request, 'compras/crear_compras.html', {
#        'r':r
        #'fabrica': fabrica
        #'data': fabrica[1],
#    })