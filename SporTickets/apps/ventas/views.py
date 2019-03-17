from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from apps.ventas.forms import SaleForm
from django.views.generic.edit import FormView
from django.forms import formset_factory

from apps.eventos.forms import EventForm, EventLocationForm
from apps.eventos.models import Event, EventLocation
from apps.ventas.forms import VentaEvento

class SaleView(FormView):
    template_name = 'ventas/ventas_form.html'
    form_class = SaleForm
    success_url = reverse_lazy("eventos:locations")#cambiar

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        event = form.cleaned_data["event"]
        eid = event.id
        print(eid)
        return redirect('ventas:buy', eid)

def TicketBuyManage(request, id_evento):#Administrar la venta de boletos
    event = get_object_or_404(Event, pk=id_evento)
    cuenta = event.event_type.localidades_del_tipo.count()

    localidades_del_tipo_de_evento = event.event_type.localidades_del_tipo.all()
 	
    TicketBuyFormSet = formset_factory(VentaEvento, extra=0, max_num=cuenta, min_num=cuenta)
    event_location_event = event.evento_localidades_del_evento.all()

    if request.method == "POST":
        formset = TicketBuyFormSet(request.POST, form_kwargs={'event' : event})
       	index = 0
       	cantidad = 0
        if formset.is_valid():
            for form in formset:
                cantidad = form.cleaned_data["cantidad"]
                index += 1
                print(cantidad)
            event.save()
            return redirect('eventos:list_event')
        else:
            print(formset.errors)

    else:
        formset = TicketBuyFormSet(form_kwargs={'event' : event})
    formsetlocations = zip(localidades_del_tipo_de_evento, formset)
    return render(request, "ventas/ventas_evento.html", {
        "formset": formset,
        "event":event,
        "locations":localidades_del_tipo_de_evento,
        "formsetlocations": formsetlocations,
        
    })
