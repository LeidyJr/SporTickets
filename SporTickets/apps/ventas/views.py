from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import DetailView, TemplateView
from django.forms import formset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from apps.boletos.models import Boleto
from apps.ventas.models import Venta
from apps.usuarios.models import User
from apps.eventos.models import Evento, LocalidadesEvento
from apps.usuarios.views import es_vendedor, es_cliente
from apps.ventas.forms import SeleccionarEventoForm, CantidadForm, SeleccionarClienteForm

@login_required
@es_cliente
def nueva_compra(request):#nueva compra
    if request.method == 'POST':
        form = SeleccionarEventoForm(request.POST)
        if form.is_valid():
            evento = form.cleaned_data["evento"]
            id_evento = evento.id
            return redirect('ventas:comprar', id_evento)
    else:
        form = SeleccionarEventoForm()
    venta_activa = Venta.obtener_venta(request)
    return render(request, 'ventas/form_compra.html', {
        'form': form,
        'venta_activa': venta_activa,
    })


@login_required
@es_cliente
def eliminar_boleto_compra(request, id_boleto):
    venta_activa = Venta.obtener_venta(request)
    boleto = get_object_or_404(Boleto, pk=id_boleto)

    if boleto in venta_activa.boletos_de_la_venta.all():
        venta_activa.eliminar_boleto(boleto)
        messages.success(request, 'Boleto eliminado exitosamente.')
    return redirect("ventas:nueva_compra")

@login_required
@es_cliente
def comprar_boletos(request, id_evento):
    evento = get_object_or_404(Evento, pk=id_evento)

    listado_localidades_evento = evento.evento_localidades_del_evento.all()
    cuenta_de_localidades_del_evento = listado_localidades_evento.count()
 	
    formset_compra_boletos = formset_factory(CantidadForm, extra=0, max_num=cuenta_de_localidades_del_evento, min_num=cuenta_de_localidades_del_evento)

    nombres_localidades_del_evento = listado_localidades_evento.values_list('localidad__nombre', flat=True)
    precios_localidades_del_evento = listado_localidades_evento.values_list('precio', flat=True)
    disponibilidad_localidades_del_evento = listado_localidades_evento.values_list('disponibilidad', flat=True)

    if request.method == "POST":
        formset = formset_compra_boletos(request.POST, form_kwargs={'evento' : evento})
        if formset.is_valid():
            venta = Venta.obtener_venta_activa(request, request.user, None)
            indice = 0
            for form in formset:
                print(form.as_table())
                localidades_evento = listado_localidades_evento[indice]
                cantidad = form.cleaned_data["cantidad"]
                if localidades_evento.disponibilidad > cantidad:
                    for _ in range(cantidad):
                        Boleto.objects.create(venta=venta, localidades_evento=localidades_evento) 
                    localidades_evento.disponibilidad -= cantidad
                    localidades_evento.save()
                else:
                    messages.error(request, 'La cantidad de boletos seleccionada no está disponible. ')
                localidades_evento.save()
                indice +=1
            evento.save()
            return redirect('ventas:nueva_compra')
        else:
            print(formset.errors)
    else:
        formset = formset_compra_boletos(form_kwargs={'evento' : evento})
    print(nombres_localidades_del_evento)
    print(formset)
    formset_y_localidades = zip(nombres_localidades_del_evento, formset)
    return render(request, "ventas/ventas_evento.html", {
        "formset": formset,
        "evento":evento,
        "localidades":nombres_localidades_del_evento,
        "formset_y_localidades": formset_y_localidades,
        "precios": precios_localidades_del_evento,
        "disponibilidad": disponibilidad_localidades_del_evento
    })

@login_required
@es_cliente
def finalizar_compra(request):
    from django.db.models import Sum
    from django.db.models.functions import Coalesce

    venta_activa = Venta.obtener_venta(request)
    boletos = venta_activa.boletos_de_la_venta.all()

    subtotal = boletos.aggregate(calc_subtotal=Coalesce(Sum("localidades_evento__precio"),0))["calc_subtotal"]
    iva = subtotal*0.19
    total = subtotal + iva

    venta_activa.subtotal = subtotal
    venta_activa.iva = iva
    venta_activa.total = total
    venta_activa.terminada = True
    venta_activa.save()
    del request.session['venta_activa']
    messages.success(request, 'Compra realizada exitosamente.')
    return redirect('ventas:factura', venta_activa.id)

@login_required
def ver_factura(request,pk):
    try:
        venta_id = Venta.objects.get(pk=pk)
    except Venta.DoesNotExist:
        raise Http404("Venta no existe")
    return render(request,'ventas/factura.html', context={'venta':venta_id,})

@login_required
@es_cliente
def mis_compras(request):
    compras = request.user.compras_del_usuario.filter(terminada=True)
    return render(request, 'ventas/listado_compras.html',{'compras':compras})

#---------------------------------------- VISTAS VENDEDOR -------------------------------------------------------------------

@login_required
@es_vendedor
def nueva_venta(request):
    if request.method == 'POST':
        form = SeleccionarEventoForm(request.POST)
        if form.is_valid():
            evento = form.cleaned_data["evento"]
            id_evento = evento.id
            return redirect('ventas:vender', id_evento)
    else:
        form = SeleccionarEventoForm()
    venta_activa = Venta.obtener_venta(request)
    return render(request, 'ventas/form_ventas.html', {
        'form': form,
        'venta_activa': venta_activa,
    })

@login_required
@es_vendedor
def vender_boletos(request, id_evento):
    evento = get_object_or_404(Evento, pk=id_evento)

    listado_localidades_evento = evento.evento_localidades_del_evento.all()
    cuenta_de_localidades_del_evento = listado_localidades_evento.count()
    
    formset_compra_boletos = formset_factory(CantidadForm, extra=0, max_num=cuenta_de_localidades_del_evento, min_num=cuenta_de_localidades_del_evento)

    nombres_localidades_del_evento = listado_localidades_evento.values_list('localidad__nombre', flat=True)
    precios_localidades_del_evento = listado_localidades_evento.values_list('precio', flat=True)
    disponibilidad_localidades_del_evento = listado_localidades_evento.values_list('disponibilidad', flat=True)

    if request.method == "POST":
        formset = formset_compra_boletos(request.POST, form_kwargs={'evento' : evento})
        if formset.is_valid():
            venta = Venta.obtener_venta_activa(request, None, request.user)
            indice = 0
            for form in formset:
                print(form.as_table())
                localidades_evento = listado_localidades_evento[indice]
                cantidad = form.cleaned_data["cantidad"]
                if localidades_evento.disponibilidad > cantidad:
                    for _ in range(cantidad):
                        Boleto.objects.create(venta=venta, localidades_evento=localidades_evento) 
                    localidades_evento.disponibilidad -= cantidad
                    localidades_evento.save()
                else:
                    messages.error(request, 'La cantidad de boletos seleccionada no está disponible. ')
                localidades_evento.save()
                indice +=1
            evento.save()
            return redirect('ventas:nueva_venta')
        else:
            print(formset.errors)
    else:
        formset = formset_compra_boletos(form_kwargs={'evento' : evento})
    print(nombres_localidades_del_evento)
    print(formset)
    formset_y_localidades = zip(nombres_localidades_del_evento, formset)
    return render(request, "ventas/ventas_evento.html", {
        "formset": formset,
        "evento":evento,
        "localidades":nombres_localidades_del_evento,
        "formset_y_localidades": formset_y_localidades,
        "precios": precios_localidades_del_evento,
        "disponibilidad": disponibilidad_localidades_del_evento
    })

@login_required
@es_vendedor
def finalizar_venta(request):

    if request.method == 'POST':
        form = SeleccionarClienteForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data["cliente"]
            print(cliente)
            print(type(cliente))
            venta_activa = Venta.obtener_venta(request)
            venta_activa.cliente = cliente

            from django.db.models import Sum
            from django.db.models.functions import Coalesce

            boletos = venta_activa.boletos_de_la_venta.all()

            subtotal = boletos.aggregate(calc_subtotal=Coalesce(Sum("localidades_evento__precio"),0))["calc_subtotal"]
            iva = subtotal*0.19
            total = subtotal + iva
            venta_activa.subtotal = subtotal
            venta_activa.iva = iva
            venta_activa.total = total
            venta_activa.terminada = True
            venta_activa.save()
            del request.session['venta_activa']
            messages.success(request, 'Venta realizada exitosamente.')
            return redirect('ventas:factura', venta_activa.id)
    else:
        form = SeleccionarClienteForm()
    venta_activa = Venta.obtener_venta(request)
    return render(request, 'ventas/cliente_form.html', {
        'form': form,
        'venta_activa': venta_activa,
    })

@login_required
@es_vendedor
def eliminar_boleto_venta(request, id_boleto):
    venta_activa = Venta.obtener_venta(request)
    boleto = get_object_or_404(Boleto, pk=id_boleto)

    if boleto in venta_activa.boletos_de_la_venta.all():
        venta_activa.eliminar_boleto(boleto)
        messages.success(request, 'Boleto eliminado exitosamente.')
    return redirect("ventas:nueva_venta")


# @login_required
# @es_vendedor
# def finalizar_venta(request):
#     from django.db.models import Sum
#     from django.db.models.functions import Coalesce

#     venta_activa = Venta.obtener_venta(request)
#     boletos = venta_activa.boletos_de_la_venta.all()

#     subtotal = boletos.aggregate(calc_subtotal=Coalesce(Sum("localidades_evento__precio"),0))["calc_subtotal"]
#     iva = subtotal*0.19
#     total = subtotal + iva

#     venta_activa.cliente = cliente
#     venta_activa.subtotal = subtotal
#     venta_activa.iva = iva
#     venta_activa.total = total
#     venta_activa.terminada = True
#     venta_activa.save()
#     del request.session['venta_activa']
#     messages.success(request, 'Venta realizada exitosamente.')
#     return redirect('ventas:factura', venta_activa.id)

