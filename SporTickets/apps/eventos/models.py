from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class TipoEvento(models.Model):

    nombre = models.CharField(max_length=100, verbose_name="Tipo de evento")

    def __str__(self):
        return (self.nombre)


class Evento(models.Model):

    ESTADO=(
		('Activo', 'Activo'),
		('Inactivo', 'Inactivo'),
        ('Cancelado', 'Cancelado'),
        ('Finalizado', 'Finalizado')
		)
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre del evento")
    descripcion = models.CharField(max_length=70, verbose_name="Descripción del evento")
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=100, verbose_name="Lugar del evento")
    url = models.URLField(max_length=100, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO, default= 'Activo')
    tipo_de_evento = models.ForeignKey(TipoEvento, related_name="eventos_del_tipo", on_delete=models.CASCADE)

    class Meta:

        ordering = ["id"]

    def __str__(self): 
        return '%s' % (self.nombre)

class Localidad(models.Model):

    nombre = models.CharField(max_length=100, verbose_name="Nombre de localidad")
    tipo_de_evento = models.ForeignKey(TipoEvento, related_name="localidades_del_tipo",verbose_name="Tipo de evento", on_delete=models.CASCADE)
    
    def __str__(self): 
        return (self.nombre)
    class Meta:
        ordering=["nombre"]


class LocalidadesEvento(models.Model):

    evento = models.ForeignKey(Evento, related_name="evento_localidades_del_evento", on_delete=models.CASCADE)
    #event.evento_localidades_del_evento = Todos los registros de EventLocation asociados a ese evento
    localidad = models.ForeignKey(Localidad, related_name="evento_localidades_de_localidades", on_delete=models.CASCADE)
    #event.evento_localidades_de_localidades = Todos los registros de EventLocation asociados a esa localidad
    capacidad = models.IntegerField()    
    precio = models.IntegerField()
    disponibilidad = models.IntegerField()

    def __str__(self): 
        return ("%s (%s)"%(self.evento, self.localidad))

    class Meta:
        ordering=["localidad__nombre"]
