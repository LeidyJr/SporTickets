from django.shortcuts import render, redirect
from functools import wraps

def es_vendedor(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.es_vendedor == True:
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrap

def es_cliente(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.es_cliente == True:
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrap

def es_gerente(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.es_gerente == True:
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrap