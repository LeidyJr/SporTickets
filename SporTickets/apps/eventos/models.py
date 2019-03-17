from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class EventType(models.Model):

    name = models.CharField(max_length=100, verbose_name="Event type")

    def __str__(self):
        return (self.name)


class Event(models.Model):

    STATUS=(
		('Activo', 'Activo'),
		('Inactivo', 'Inactivo'),
        ('Cancelado', 'Cancelado'),
        ('Finalizado', 'Finalizado')
		)
    
    name = models.CharField(max_length=100, verbose_name="Event's name")
    description = models.CharField(max_length=70, verbose_name="Event's description")
    event_date = models.DateField()
    event_time = models.TimeField()
    event_place = models.CharField(max_length=100, verbose_name="Location")
    event_url = models.URLField(max_length=100, blank=True)
    event_status = models.CharField(max_length=20, choices=STATUS, default= 'Activo')
    event_type= models.ForeignKey(EventType, related_name="eventos_del_tipo", on_delete=models.CASCADE)

    class Meta:

        ordering = ["id"]

    def __str__(self): 
        return '%s' % (self.name)


class Location(models.Model):

    name = models.CharField(max_length=100, verbose_name="Location's name")
    event_type = models.ForeignKey(EventType,related_name="localidades_del_tipo",verbose_name="Event type", on_delete=models.CASCADE)

    def __str__(self): 
        return (self.name)
    class Meta:
        ordering=["name"]


class EventLocation(models.Model):

    event = models.ForeignKey(Event, related_name="evento_localidades_del_evento", on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name="evento_localidades_de_localidades", on_delete=models.CASCADE)
    capacity = models.IntegerField()    
    price = models.IntegerField()
    availability = models.IntegerField()

    def __str__(self): 
        return ("%s (%s)"%(self.event, self.location))

    class Meta:
        ordering=["location__name"]
