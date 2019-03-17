from django import forms

from apps.ventas.models import Sale
from apps.eventos.models import EventType, Event, Location, EventLocation
from apps.boletos.models import Ticket

class SaleForm(forms.Form):
    event = forms.ModelChoiceField(queryset = Event.objects.all().filter(event_status='Activo') )

    def clean_price(self):
        data = self.cleaned_data.get('event')
        return event

class VentaEvento(forms.Form):

	 cantidad = forms.IntegerField(label='Cantidad: ', initial =0)

	 def __init__(self, *args, event, **kwargs):
	 	self.event = event
	 	super(VentaEvento, self).__init__(*args, **kwargs)

