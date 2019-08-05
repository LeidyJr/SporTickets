# from django.shortcuts import render
# from django.views.generic import View

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions

# from apps.usuarios.models import User

# class ChartData(APIView):
# 	authentication_classes = []
# 	permission_classes = []

# 	def get(self, request, format=None):
# 		nombres_vendedores = [vendedor.username for vendedor in User.objects.filter(es_vendedor=True)]
# 		return Response(nombres_vendedores)


from apps.eventos.models import Evento, LocalidadesEvento
from apps.ventas.models import Venta
from apps.boletos.models import Boleto
from django.db.models import *
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from apps.usuarios.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


class BoletosPorEventoVista(BaseLineChartView):
    def get_labels(self):
        nombres_eventos = list(Evento.objects.all().values_list("nombre", flat=True))
        return nombres_eventos

    def get_providers(self):
        return ["Boletos vendidos"]

    def get_data(self):
        eventos = Evento.objects.all()
        boletos_vendidos_eventos = []
        for evento in eventos:
            boletos_vendidos_evento = evento.evento_localidades_del_evento.aggregate(conteo=Count('boletos_de_event_location'))["conteo"]
            boletos_vendidos_eventos.append(boletos_vendidos_evento)
        return [boletos_vendidos_eventos]

vista_boletos_por_evento = TemplateView.as_view(template_name='reportes/boletos_por_evento.html')
boletos_por_evento_json = BoletosPorEventoVista.as_view()


class VentasPorVendedor(BaseLineChartView):
    def get_labels(self):
        nombres_vendedores = list(User.objects.filter(es_vendedor=True).values_list("username", flat=True))
        return nombres_vendedores

    def get_providers(self):
        return ["Ventas realizadas"]

    def get_data(self):
        vendedores = User.objects.filter(es_vendedor=True)
        ventas_de_vendedores = []
        for vendedor in vendedores:
            ventas_del_vendedor = vendedor.ventas_del_vendedor.count()
            ventas_de_vendedores.append(ventas_del_vendedor)
        return [ventas_de_vendedores]

vista_ventas_por_vendedor = TemplateView.as_view(template_name='reportes/ventas_por_vendedor.html')
ventas_por_vendedor_json = VentasPorVendedor.as_view()
