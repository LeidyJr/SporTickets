from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include


from .views import *

app_name='ventas'
urlpatterns = [
    
    url(regex=r"^compra$", view=nueva_compra, name="nueva_compra"),
    url(regex=r"^venta$", view=nueva_venta, name="nueva_venta"),

    url(regex=r"^eliminar-boleto-compra/(?P<id_boleto>[\w-]+)$", view=eliminar_boleto_compra, name="eliminar_boleto_compra"),
    url(regex=r"^eliminar-boleto-venta/(?P<id_boleto>[\w-]+)$", view=eliminar_boleto_venta, name="eliminar_boleto_venta"),

    url(regex=r"^finalizar-compra$", view=finalizar_compra, name="finalizar_compra"),
    url(regex=r"^finalizar-venta$", view=finalizar_venta, name="finalizar_venta"),

    url(regex=r"^comprar/(?P<id_evento>[\w-]+)$", view=comprar_boletos, name="comprar"),
    url(regex=r"^vender/(?P<id_evento>[\w-]+)$", view=vender_boletos, name="vender"),

    url(r'^factura/(?P<pk>\d+)/$', view=ver_factura, name='factura'),

    url(r'^mis-compras$', view=mis_compras, name='mis_compras'),
]

