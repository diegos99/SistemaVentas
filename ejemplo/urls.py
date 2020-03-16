from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    
    path('clientes/create_update_clientes.html', views.formularioAgregarObjeto),
    path('clientes/lista_cliente.html', views.lista_objetos),
    path('editar_cliente/<int:objeto_id>', views.editarObjeto),
    path('eliminar_cliente/<int:objeto_id>', views.eliminarObjeto),
    path('detalle_clientes/<int:objeto_id>', views.detalle_objetos),
]