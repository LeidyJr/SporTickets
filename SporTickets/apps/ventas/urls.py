from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include


from .views import *

app_name='ventas'
urlpatterns = [
    
    url(regex=r"^$", view=nueva_compra, name="nueva_compra"),
    url(regex=r"^eliminar-boleto/(?P<id_boleto>[\w-]+)$", view=eliminar_boleto, name="eliminar_boleto"),
    url(regex=r"^finalizar-compra$", view=finalizar_compra, name="finalizar_compra"),
    url(regex=r"^comprar/(?P<id_evento>[\w-]+)$", view=comprar_boletos, name="comprar"),
    url(r'^factura/(?P<pk>\d+)/$', view=ver_factura, name='factura'),
    url(r'^mis-compras$', view=mis_compras, name='mis_compras'),
]

