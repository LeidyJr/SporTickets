from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
import datetime

from apps.eventos.models import TipoEvento, Evento, Localidad, LocalidadesEvento 

class EventoForm(forms.ModelForm):

	fecha = forms.DateField(
        widget=DatePickerInput(format='%d-%m-%Y'),
        input_formats = ['%d-%m-%Y']
    )

	class Meta:
		model = Evento
		fields = ("nombre" , "descripcion", "fecha", "hora", "lugar","url", "estado","tipo_de_evento", )
		labels = {
		"nombre": "Nombre: ",
		"descripcion": "Descripción: ", 
		"fecha": "Fecha: ",
		"hora": "Hora: ",
		"lugar": "Lugar: ",
		"url": "Url: ",
		"estado": "Estado: ", 
		"tipo_de_evento": "Tipo de evento: "
		}
		widgets = {
		"fecha" : DatePickerInput(),
		"hora" : TimePickerInput(),
		}

	def __init__(self, *args, **kwargs):
		super(EventoForm, self).__init__(*args, **kwargs)
        #self.fields['imagen'].required = False

	def clean_event_date(self):
		data = self.cleaned_data.get('fecha', '')
		date_aux_str = self.data['fecha']
		date_aux = datetime.datetime.strptime(date_aux_str, '%d-%m-%Y')
		if not date_aux > datetime.datetime.now():
			raise ValidationError("La fecha del evento debe ser mayor a la fecha actual")
		return data


class LocalidadesEventoForm(forms.ModelForm):

	def __init__(self, *args, evento, **kwargs):
		self.evento = evento
		super(LocalidadesEventoForm, self).__init__(*args, **kwargs)

	class Meta:

		model = LocalidadesEvento
		fields = ("capacidad","precio")
		labels = {"capacidad" : "Capacidad: ", "precio" : "Precio: ", }