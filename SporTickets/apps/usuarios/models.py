from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    es_vendedor = models.BooleanField(default=False)
    es_cliente = models.BooleanField(default=False)
    es_gerente = models.BooleanField(default=False)
    es_administrador = models.BooleanField(default=False)


    def obtener_perfil_vendedor(self):
        perfil_vendedor = None
        if hasattr(self, 'perfilvendedor'):
            perfil_vendedor = self.perfilvendedor
        return perfil_vendedor

    def obtener_perfil_cliente(self):
        perfil_cliente = None
        if hasattr(self, 'perfilcliente'):
            perfil_cliente = self.perfilcliente
        return perfil_cliente

    def obtener_perfil_gerente(self):
        obtener_perfil_gerente = None
        if hasattr(self, 'perfilgerente'):
            obtener_perfil_gerente = self.perfilgerente
        return obtener_perfil_gerente

    def obtener_perfil_administrador(self):
        obtener_perfil_administrador = None
        if hasattr(self, 'perfiladministrador'):
            obtener_perfil_administrador = self.perfiladministrador
        return obtener_perfil_administrador

    class Meta:
        db_table = 'auth_user'


class PerfilVendedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    cedula = models.CharField(max_length=10, unique=True)


class PerfilCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    cedula = models.CharField(max_length=10, unique=True)

class PerfilGerente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    cedula = models.CharField(max_length=10, unique=True)

class perfiladministrador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    cedula = models.CharField(max_length=10, unique=True)