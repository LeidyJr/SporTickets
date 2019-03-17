from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView,
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError

from apps.eventos.forms import EventForm, EventLocationForm
from apps.eventos.models import Event, EventLocation
from apps.boletos.models import Ticket
from apps.ventas.models import Sale


class TicketCreate(CreateView):
    model = Ticket
    form_class = EventForm
    template_name = "eventos/eventos_form.html"
    success_url = reverse_lazy("eventos:locations")
            
    def get_success_url(self):
        return reverse_lazy("eventos:locations", kwargs={"id_evento": self.object.id})

