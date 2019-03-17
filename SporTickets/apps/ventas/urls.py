from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include


from .views import SaleView, TicketBuyManage

app_name='ventas'
urlpatterns = [
    
    url(regex=r"^create$", view=SaleView.as_view(), name="sale_create"),
    url(regex=r"^buy/(?P<id_evento>[\w-]+)$", view=TicketBuyManage, name="buy"),
]