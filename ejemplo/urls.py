from django.urls import path, include
from . import views
from .views import *
urlpatterns = [
    path('', views.index),
    path('login', views.loginPage, name='login'),
    path('register', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),

    # TIPO DE CLIENTE
    path('clientes/create_tipo_cliente.html', views.formularioAgregarTipoCliente),
    path('clientes/lista_tipo_cliente.html', views.lista_tipo_clientes),
    path('create_tipo_cliente/<int:tipo_cliente_id>', views.editarTipoCliente),

    # CLIENTE
    path('clientes/create_update_clientes.html', views.formularioAgregarCliente),
    path('clientes/lista_cliente.html', views.lista_clientes),
    path('detalle_clientes/<int:cliente_id>', views.detalle_clientes),
    path('editar_cliente/<int:cliente_id>', views.editarCliente),
    path('eliminar_cliente/<int:cliente_id>', views.eliminarCliente),

    # SUSCRIPCIONES
    path('suscripciones/create_suscrip.html', views.formularioAgregarSuscrip),
    path('suscripciones/lista_suscrip.html', views.lista_suscripciones),
    path('detalle_suscrip/<int:suscripcion_id>', views.detalle_suscrip),
    path('editar_suscrip/<int:suscripcion_id>', views.editarSuscripcion),
    path('eliminar_suscrip/<int:suscripcion_id>', views.eliminarSuscripcion),

    # FABRICAS
    path('fabricas/create_fabricas.html', views.formularioAgregarFabrica),
    path('fabricas/lista_fabricas.html', views.lista_fabricas),
    path('detalle_fabricas/<int:fabrica_id>', views.detalle_fabricas),
    path('editar_fabricas/<int:fabrica_id>', views.editarFabrica),
    path('eliminar_fabricas/<int:fabrica_id>', views.eliminarFabrica),

    # REPUESTOS
    path('repuestos/create_repuestos.html', views.formularioAgregarRepuesto),
    #path('repuestos/lista_repuestos.html', views.lista_repuestos),
    path('repuestos/lista_repuestos.html', lista_repuestos.as_view(), name = 'lista_repuestos'),
    path('detalle_repuestos/<int:repuesto_id>', views.detalle_repuestos),
    path('editar_repuestos/<int:repuesto_id>', views.editarRepuesto),
    path('eliminar_repuestos/<int:repuesto_id>', views.eliminarRepuesto),

    # VEHICULOS
    path('vehiculos/create_vehiculos.html', views.formularioAgregarVehiculo),
    path('vehiculos/lista_vehiculos.html', views.lista_vehiculos),
    path('detalle_vehiculos/<int:vehiculo_id>', views.detalle_vehiculos),
    path('editar_vehiculos/<int:vehiculo_id>', views.editarVehiculo),
    path('eliminar_vehiculos/<int:vehiculo_id>', views.eliminarVehiculo),

    # COMPATIBILIDAD
    path('compat/create_compat.html', views.formularioAgregarCompat),
    path('compat/lista_compat.html', views.lista_compats),
    path('detalle_compat/<int:compatibilidad_id>', views.detalle_compats),
    path('editar_compat/<int:compatibilidad_id>', views.editarCompat),
    path('eliminar_compat/<int:compatibilidad_id>', views.eliminarCompat),

    # FACTURAS
    path('factura/crear_factura.html', views.facturaCrear),
    path('factura/buscar_cliente', views.buscarCliente),
    path('factura/buscar_producto', views.buscarProducto),
    path('factura/crear_factura', views.facturaCrear),
    path('factura/lista_venta.html', ListaVentas.as_view(), name = 'ListaVentas'),
    path('reporte_venta/<int:pk>', views.reporteventas),

    # ORDENES
    path('orden/crear_factura.html', views.ordenCrear),
    path('orden/buscar_cliente', views.buscarClient),
    path('orden/buscar_producto', views.buscarProduct),
    path('orden/crear_factura', views.ordenCrear),
    path('orden/lista_venta.html', ListaOrdenes.as_view(), name = 'ListaOrdenes'),
    path('reporte_orden/<int:pk>', views.reporteordenes),
]