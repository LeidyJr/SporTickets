from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from .views import *

app_name='usuarios'

urlpatterns = [
    url('signup', signup, name='signup'),
    url(regex=r"^listado$", view=es_administrador(ListarClientes.as_view()), name="listado_de_clientes"),
    url(r'^editar/(?P<pk>\d+)/$', es_administrador(EditarCliente.as_view()), name='editar_usuario'),
]