from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from apps.ventas.forms import SelectEventForm
from django.views.generic.edit import FormView
from django.forms import formset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from apps.eventos.forms import EventForm, EventLocationForm
from apps.eventos.models import Event, EventLocation
from apps.boletos.models import Ticket
from apps.ventas.models import Sale
from apps.ventas.forms import TicketsForm

def new_sale(request):
    if request.method == 'POST':
        form = SelectEventForm(request.POST)
        if form.is_valid():
            event = form.cleaned_data["event"]
            event_id = event.id
            return redirect('ventas:buy', event_id)
    else:
        form = SelectEventForm()
    venta_activa = Sale.obtener_sale(request)
    return render(request, 'ventas/ventas_form.html', {
        'form': form,
        'venta_activa': venta_activa,
    })

def eliminar_boleto(request, id_boleto):
    venta_activa = Sale.obtener_sale(request)
    boleto = get_object_or_404(Ticket, pk=id_boleto)

    if boleto in venta_activa.boletos_de_la_venta.all():
        venta_activa.eliminar_boleto(boleto)
        messages.success(request, 'Boleto eliminado exitosamente.')
    return redirect("ventas:sale_create")

@login_required
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
                if event_location.availability > cantidad:
                    for _ in range(cantidad):
                        Ticket.objects.create(sale=sale, event_location=event_location) 
                    event_location.availability -= cantidad
                    event_location.save()
                    
                else:
                    print("No hay tantos boletos")
                    messages.error(request, 'La cantidad de boletos seleccionada no está disponible. ')
                event_location.save()
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

def finalizar_compra(request):
    from django.db.models import Sum
    from django.db.models.functions import Coalesce

    venta_activa = Sale.obtener_sale(request)
    boletos = venta_activa.boletos_de_la_venta.all()

    subtotal = boletos.aggregate(calc_subtotal=Coalesce(Sum("event_location__price"),0))["calc_subtotal"]
    iva = subtotal*0.19
    total = subtotal + iva

    venta_activa.subtotal = subtotal
    venta_activa.iva = iva
    venta_activa.total = total
    venta_activa.finished = True
    venta_activa.save()
    del request.session['venta_activa']
    messages.success(request, 'Compra realizada exitosamente.')
    return redirect('ventas:sale_create')

