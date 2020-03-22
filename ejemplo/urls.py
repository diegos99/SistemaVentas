from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
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
]