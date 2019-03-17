from django.contrib import admin
from .models import Event, EventType, Location, EventLocation

# Register your models here.

admin.site.register(Event)
admin.site.register(EventType)
admin.site.register(Location)
admin.site.register(EventLocation)