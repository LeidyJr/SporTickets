from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
import datetime

from apps.eventos.models import EventType, Event, Location, EventLocation 

class EventForm(forms.ModelForm):

	event_date = forms.DateField(
        widget=DatePickerInput(format='%d-%m-%Y'),
        input_formats = ['%d-%m-%Y']
    )

	class Meta:
		model = Event
		fields = ("name" , "description", "event_date", "event_time", "event_place","event_url", "event_status","event_type", )
		labels = {
		"name": "Nombre: ",
		"description": "Descripción: ", 
		"event_date": "Fecha: ",
		"event_time": "Hora: ",
		"event_place": "Lugar: ",
		"event_url": "Url: ",
		"event_status": "Estado: ", 
		"event_type": "Tipo de evento: "
		}
		widgets = {
		"event_date" : DatePickerInput(),
		"event_time" : TimePickerInput(),
		}

	def __init__(self, *args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)
        #self.fields['imagen'].required = False

	def clean_event_date(self):
		data = self.cleaned_data.get('event_date', '')
		date_aux_str = self.data['event_date']
		date_aux = datetime.datetime.strptime(date_aux_str, '%d-%m-%Y')
		if not date_aux > datetime.datetime.now():
			raise ValidationError("La fecha del evento debe ser mayor a la fecha actual")
		return data


class EventLocationForm(forms.ModelForm):

	def __init__(self, *args, event, **kwargs):
		self.event = event
		super(EventLocationForm, self).__init__(*args, **kwargs)

	class Meta:

		model = EventLocation
		fields = ("capacity","price")
		labels = {"capacity" : "Capacidad: ", "price" : "Precio: ", }