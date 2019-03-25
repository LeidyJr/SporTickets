from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from functools import wraps

from apps.usuarios.forms import SignUpForm, EditUserForm
from apps.usuarios.models import User

def es_vendedor(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.es_vendedor == True:
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap

def es_cliente(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.es_cliente == True:
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap

def es_gerente(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.es_gerente == True:
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap

def es_administrador(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.es_administrador == True:
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.es_cliente =True
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'usuarios/signup.html', {'form': form})



class ListarClientes(LoginRequiredMixin, ListView):
    model = User
    template_name = 'usuarios/listado_clientes.html'
    queryset = User.objects.filter(es_cliente=True)


class EditarCliente(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'usuarios/editar_usuario.html'
    success_message = "El usuario %(username)s se modificó correctamente."
    success_url = reverse_lazy('usuarios:listado_de_clientes')