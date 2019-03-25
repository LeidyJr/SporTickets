from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from apps.eventos.forms import EventoForm, LocalidadesEventoForm
from apps.eventos.models import Evento, LocalidadesEvento, Localidad
from apps.usuarios.views import es_administrador
# Create your views here.

@login_required
def index(request):
    return render(request, 'eventos/index.html')


class CrearEvento(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = "eventos/eventos_form.html"
    success_message = "El evento %(nombre)s se registró correctamente."
    success_url = reverse_lazy("eventos:localidades")
            
    def get_success_url(self):
        return reverse_lazy("eventos:localidades", kwargs={"id_evento": self.object.id})

class ListarEventos(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'eventos/eventos_list.html'
    queryset = Evento.objects.all()


class EditarEvento(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/eventos_form.html'
    success_message = "El evento %(name)s se modificó correctamente."
    success_url = reverse_lazy('eventos:listado_de_eventos')


@login_required
@es_administrador
def AdministrarLocalidadesEvento(request, id_evento):
    evento = get_object_or_404(Evento, pk=id_evento)

    cuenta_de_localidades_del_tipo_de_evento = evento.tipo_de_evento.localidades_del_tipo.count()
    localidades_del_tipo_de_evento = evento.tipo_de_evento.localidades_del_tipo.all()

    formset_localidades_del_evento = modelformset_factory(LocalidadesEvento, form=LocalidadesEventoForm, max_num=cuenta_de_localidades_del_tipo_de_evento, min_num=cuenta_de_localidades_del_tipo_de_evento, extra=0)
    localidades_del_evento = evento.evento_localidades_del_evento.all()

    if request.method == "POST":
        formset = formset_localidades_del_evento(request.POST, form_kwargs={'evento' : evento})
        indice = 0
        if formset.is_valid():
            for form in formset:
                localidad_evento = form.save(commit=False)
                localidad_evento.evento = evento 
                localidad_evento.localidad = localidades_del_tipo_de_evento[indice]
                localidad_evento.disponibilidad = localidad_evento.capacidad 
                localidad_evento.save()
                indice += 1
            evento.save()
            messages.success(request, 'Las localidades se registraron correctamente.')
            return redirect('eventos:listado_de_eventos')
        else:
            messages.warning(request, 'Por favor verifique que todos los campos se hayan diligenciado correctamente.')
    else:
        formset = formset_localidades_del_evento(form_kwargs={'evento' : evento}, queryset=localidades_del_evento)
    formset_y_localidades = zip(localidades_del_tipo_de_evento, formset)
    return render(request, "eventos/localidad_evento_form.html", {
        "formset": formset,
        "evento":evento,
        "localidades":localidades_del_tipo_de_evento,
        "formset_y_localidades": formset_y_localidades,
    })

