from django import forms

from apps.ventas.models import Venta
from apps.eventos.models import TipoEvento, Evento, Localidad, LocalidadesEvento
from apps.boletos.models import Boleto
from apps.usuarios.models import User

class SeleccionarEventoForm(forms.Form):
    evento = forms.ModelChoiceField(queryset = Evento.objects.all().filter(estado='Activo'))
    def clean_price(self):
        data = self.cleaned_data.get('evento')
        return data


class CantidadForm(forms.Form):

	 cantidad = forms.IntegerField(label='Cantidad: ', initial =0)

	 def __init__(self, *args, evento, **kwargs):
	 	self.evento = evento
	 	super(CantidadForm, self).__init__(*args, **kwargs)

class SeleccionarClienteForm(forms.Form):

	cliente = forms.ModelChoiceField(queryset = User.objects.all().filter(es_cliente=True))

	def clean_cliente(self):
		data = self.cleaned_data.get('cliente')
		return data