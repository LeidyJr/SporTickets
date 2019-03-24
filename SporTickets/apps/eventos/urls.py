from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from .views import index, CrearEvento, ListarEventos, EditarEvento, AdministrarLocalidadesEvento

app_name='eventos'

urlpatterns = [
    url('index', index, name='index'),
    url(regex=r"^registrar$", view=CrearEvento.as_view(), name="registrar_evento"),
    url(regex=r"^listado$", view=ListarEventos.as_view(), name="listado_de_eventos"),
    url(r'^editar/(?P<pk>\d+)/$', EditarEvento.as_view(), name='editar_evento'),
    url(regex=r"^localidades/(?P<id_evento>[\w-]+)$", view=AdministrarLocalidadesEvento, name="localidades"),
]