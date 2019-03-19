from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from apps.ventas.forms import SelectEventForm
from django.views.generic.edit import FormView
from django.forms import formset_factory

from apps.eventos.forms import EventForm, EventLocationForm
from apps.eventos.models import Event, EventLocation
from apps.boletos.models import Ticket
from apps.ventas.models import Sale
from apps.ventas.forms import TicketsForm

class SaleView(FormView):
    template_name = 'ventas/ventas_form.html'
    form_class = SelectEventForm
    success_url = reverse_lazy("eventos:locations")#cambiar

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        event = form.cleaned_data["event"]
        event_id = event.id
        print(event_id)
        return redirect('ventas:buy', event_id)

def TicketBuyManage(request, id_evento):#Administrar la venta de boletos para un evento.
    event = get_object_or_404(Event, pk=id_evento)

    listado_event_location = event.evento_localidades_del_evento.all()

    cuenta_de_localidades_del_evento = listado_event_location.count()
 	
    TicketBuyFormSet = formset_factory(TicketsForm, extra=0, max_num=cuenta_de_localidades_del_evento, min_num=cuenta_de_localidades_del_evento)

    nombres_localidades_del_evento = listado_event_location.values_list('location__name', flat=True)
    precios_localidades_del_evento = listado_event_location.values_list('price', flat=True)
    disponibilidad_localidades_del_evento = listado_event_location.values_list('capacity', flat=True)

    if request.method == "POST":
        formset = TicketBuyFormSet(request.POST, form_kwargs={'event' : event})
        if formset.is_valid():
            sale = Sale.obtener_sale_active(request, "nombre_cliente", "nombre_vendedor")
            index=0
            for form in formset:
                event_location = listado_event_location[index]
                cantidad = form.cleaned_data["cantidad"]
                if event_location.availability > 0: 
                    event_location.availability -= cantidad
                else:
                    print("No hay tantos boletos")
                event_location.save()
                for _ in range(cantidad):
                    Ticket.objects.create(sale=sale, event_location=event_location)
                index +=1
            event.save()
            return redirect('ventas:sale_create')
        else:
            print(formset.errors)

    else:
        formset = TicketBuyFormSet(form_kwargs={'event' : event})
    formsetlocations = zip(nombres_localidades_del_evento, formset)
    return render(request, "ventas/ventas_evento.html", {
        "formset": formset,
        "event":event,
        "locations":nombres_localidades_del_evento,
        "formsetlocations": formsetlocations,
        "prices": precios_localidades_del_evento,
        "disponibility": disponibilidad_localidades_del_evento
    })
