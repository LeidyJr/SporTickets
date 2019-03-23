from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include


from .views import *

app_name='ventas'
urlpatterns = [
    
    url(regex=r"^create$", view=new_sale, name="sale_create"),
    url(regex=r"^eliminar-boleto/(?P<id_boleto>[\w-]+)$", view=eliminar_boleto, name="eliminar_boleto"),
    url(regex=r"^finalizar-compra$", view=finalizar_compra, name="finalizar_compra"),
    url(regex=r"^buy/(?P<id_evento>[\w-]+)$", view=TicketBuyManage, name="buy"),
]

