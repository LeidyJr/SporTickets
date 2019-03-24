from django.contrib import admin
from .models import Evento, TipoEvento, Localidad, LocalidadesEvento

# Register your models here.

admin.site.register(Evento)
admin.site.register(TipoEvento)
admin.site.register(Localidad)
admin.site.register(LocalidadesEvento)