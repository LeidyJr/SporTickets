from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from .views import index, CrearEvento, ListarEventos, EditarEvento, AdministrarLocalidadesEvento
from apps.usuarios.views import es_vendedor, es_cliente, es_gerente, es_administrador

app_name='eventos'

urlpatterns = [
    url('index', index, name='index'),
    url(regex=r"^registrar$", view=es_administrador(CrearEvento.as_view()), name="registrar_evento"),
    url(regex=r"^listado$", view=ListarEventos.as_view(), name="listado_de_eventos"),
    url(r'^editar/(?P<pk>\d+)/$', es_administrador(EditarEvento.as_view()), name='editar_evento'),
    url(regex=r"^localidades/(?P<id_evento>[\w-]+)$", view=AdministrarLocalidadesEvento, name="localidades"),
]