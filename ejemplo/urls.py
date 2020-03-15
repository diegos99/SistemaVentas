from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('ejemplo/agregarObjeto.html', views.formularioAgregarObjeto),
    path('ejemplo/listaObjeto.html', views.lista_objetos),
    path('editarObjeto/<int:objeto_id>', views.editarObjeto),
    path('eliminarObjeto/<int:objeto_id>', views.eliminarObjeto),
]