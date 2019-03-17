from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.forms import modelformset_factory

from apps.eventos.forms import EventForm, EventLocationForm
from apps.eventos.models import Event, EventLocation, Location
from apps.boletos.models import Ticket
from apps.ventas.models import Sale
# Create your views here.

def index(request):
    return render(request, 'eventos/index.html')

class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    template_name = "eventos/eventos_form.html"
    success_url = reverse_lazy("eventos:locations")
            
    def get_success_url(self):
        return reverse_lazy("eventos:locations", kwargs={"id_evento": self.object.id})

class EventList(ListView):
    model = Event
    template_name = 'eventos/eventos_list.html'
    #paginate_by = 2


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'eventos/eventos_form.html'
    success_url = reverse_lazy('eventos:list_event')

class EventDelete(DeleteView):
    model = Event
    template_name = 'eventos/eventos_delete.html'
    success_url = reverse_lazy('eventos:list_event')

def EventLocationManage(request, id_evento):
    event = get_object_or_404(Event, pk=id_evento)
    cuenta_de_localidades_del_tipo_de_evento = event.event_type.localidades_del_tipo.count()

    localidades_del_tipo_de_evento = event.event_type.localidades_del_tipo.all()
    event_location_formset = modelformset_factory(EventLocation, form=EventLocationForm, max_num=cuenta_de_localidades_del_tipo_de_evento, min_num=cuenta_de_localidades_del_tipo_de_evento, extra=0)
    event_location_event = event.evento_localidades_del_evento.all()

    if request.method == "POST":
        formset = event_location_formset(request.POST, form_kwargs={'event' : event})
        index = 0
        if formset.is_valid():
            for form in formset:
                event_location = form.save(commit=False)
                event_location.event = event
                event_location.location = localidades_del_tipo_de_evento[index]
                event_location.availability = event_location.capacity
                event_location.save()
                index += 1
            event.save()
            return redirect('eventos:list_event')
        else:
            print(formset.errors)
    else:
        formset = event_location_formset(form_kwargs={'event' : event}, queryset=event_location_event)
    formsetlocations = zip(localidades_del_tipo_de_evento, formset)
    return render(request, "eventos/localidad_evento_form.html", {
        "formset": formset,
        "event":event,
        "locations":localidades_del_tipo_de_evento,
        "formsetlocations": formsetlocations,
    })

