from django.shortcuts import render, redirect
from functools import wraps

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


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from apps.usuarios.forms import SignUpForm

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