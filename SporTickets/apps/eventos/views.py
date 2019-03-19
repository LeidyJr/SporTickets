from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from apps.eventos.forms import EventForm, EventLocationForm
from apps.eventos.models import Event, EventLocation, Location
from apps.boletos.models import Ticket
from apps.ventas.models import Sale
# Create your views here.

def index(request):
    return render(request, 'eventos/index.html')

class EventCreate(SuccessMessageMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "eventos/eventos_form.html"
    success_message = "El evento %(name)s se registró correctamente."
    success_url = reverse_lazy("eventos:locations")
            
    def get_success_url(self):
        return reverse_lazy("eventos:locations", kwargs={"id_evento": self.object.id})

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            name=self.object.name,
        )

class EventList(ListView):
    model = Event
    template_name = 'eventos/eventos_list.html'
    queryset = Event.objects.all()
    #filter(event_status='Activo')
    #paginate_by = 2


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'eventos/eventos_form.html'
    success_message = "El evento %(name)s se modificó correctamente."
    success_url = reverse_lazy('eventos:list_event')

class EventDelete(DeleteView):
    model = Event
    template_name = 'eventos/eventos_delete.html'
    success_url = reverse_lazy('eventos:list_event')

def EventLocationManage(request, id_evento):
    event = get_object_or_404(Event, pk=id_evento)#Instancia de evento, pues las EventLocation se crean/modifican dependiendo del evento.

    cuenta_de_localidades_del_tipo_de_evento = event.event_type.localidades_del_tipo.count()#Cuento las localidades del tipo de ese evento.
    localidades_del_tipo_de_evento = event.event_type.localidades_del_tipo.all()#Traigo todas las localidades del tipo de ese evento.

    event_location_formset = modelformset_factory(EventLocation, form=EventLocationForm, max_num=cuenta_de_localidades_del_tipo_de_evento, min_num=cuenta_de_localidades_del_tipo_de_evento, extra=0)
    #Creo un formset, va a crear objetos del tipo EvntLocation, con el formulario EventLocationForm, cantidad = cuenta de localidades de ese tipo de evento.
    event_location_event = event.evento_localidades_del_evento.all()#Traigo todos los EventLocation del evento.

    if request.method == "POST":#Si se va a crear
        formset = event_location_formset(request.POST, form_kwargs={'event' : event})#Le paso al formset el evento.
        index = 0
        if formset.is_valid():
            for form in formset:#Para cada formulario dentro del formset, haga lo siguiente:
                event_location = form.save(commit=False)#Devuelve un objeto que aún no será guardado en la BD
                event_location.event = event #El evento es el ingresado
                event_location.location = localidades_del_tipo_de_evento[index] # Cada una de las localidades del tipo de evento
                event_location.availability = event_location.capacity #La disponibilidad inicial,es igual a la capacidad
                event_location.save()#Guarda el objeto en la BD
                messages.success(request, 'Las localidades se registraron correctamente.')
                index += 1
            event.save()
            return redirect('eventos:list_event')
        else:
            messages.warning(request, 'Por favor verifique que todos los campos se hayan diligenciado correctamente.')
    else:#Si se va a modificar
        formset = event_location_formset(form_kwargs={'event' : event}, queryset=event_location_event)
    formsetlocations = zip(localidades_del_tipo_de_evento, formset)
    return render(request, "eventos/localidad_evento_form.html", {
        "formset": formset,
        "event":event,
        "locations":localidades_del_tipo_de_evento,
        "formsetlocations": formsetlocations,
    })

