from django.db import models

from apps.eventos.models import LocalidadesEvento
from apps.ventas.models import Venta

class ManejadorBoletos(models.Manager):
    def crear_boleto(self, localidades_evento, venta):
        boleto = self.create(localidades_evento=localidades_evento)
        return boleto

class Boleto(models.Model):
	venta = models.ForeignKey(Venta, related_name="boletos_de_la_venta",verbose_name="Venta", on_delete=models.CASCADE)
	localidades_evento = models.ForeignKey(LocalidadesEvento, related_name="boletos_de_event_location", verbose_name="LocalidadesEvento", on_delete=models.CASCADE)
	objects = ManejadorBoletos()

	
	
