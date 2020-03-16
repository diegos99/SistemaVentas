from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    
    path('clientes/create_update_clientes.html', views.formularioAgregarObjeto),
    path('clientes/lista_cliente.html', views.lista_objetos),
    path('editarObjeto/<int:objeto_id>', views.editarObjeto),
    path('eliminarObjeto/<int:objeto_id>', views.eliminarObjeto),
]