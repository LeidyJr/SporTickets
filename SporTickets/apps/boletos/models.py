from django.db import models

from apps.eventos.models import EventLocation
from apps.ventas.models import Sale




class TicketManager(models.Manager):
    def create_ticket(self, event_location, sale):
        ticket = self.create(event_location=event_location)
        # do something with the book
        return ticket

class Ticket(models.Model):
	sale = models.ForeignKey(Sale,related_name="boletos_de_la_venta",verbose_name="Sale", on_delete=models.CASCADE)
	event_location = models.ForeignKey(EventLocation, related_name="boletos_de_event_location", verbose_name="EventLocation", on_delete=models.CASCADE)

	objects = TicketManager()

	
	
