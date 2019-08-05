from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from apps.usuarios.views import *
from .views import *

app_name='reportes'

urlpatterns = [
    #url(r'^api/data/$', view=ChartData.as_view(), name="api-data"),
    path('boletos_por_evento', es_gerente(vista_boletos_por_evento), name="boletos_por_evento"),
    path('boletos_por_evento_json', es_gerente(boletos_por_evento_json), name="boletos_por_evento_json"),
    path('ventas_por_vendedor', es_gerente(vista_ventas_por_vendedor), name="ventas_por_vendedor"),
    path('ventas_por_vendedor_json', es_gerente(ventas_por_vendedor_json), name="ventas_por_vendedor_json"),
]