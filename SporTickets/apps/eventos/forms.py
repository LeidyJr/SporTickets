from django import forms
from apps.eventos.models import EventType, Event, Location, EventLocation #Llamo al modelo que se va a utilizar
from bootstrap_datepicker_plus import DatePickerInput

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
		}

	def __init__(self, *args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)
        #self.fields['imagen'].required = False


class EventLocationForm(forms.ModelForm):

	def __init__(self, *args, event, **kwargs):
		self.event = event
		super(EventLocationForm, self).__init__(*args, **kwargs)

	class Meta:

		model = EventLocation
		fields = ("capacity","price")
		labels = {"capacity" : "Capacidad: ", "price" : "Precio: ", }