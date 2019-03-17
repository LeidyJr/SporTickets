from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from .views import index, EventList, EventCreate, EventUpdate, EventDelete, EventLocationManage #llama la vista

app_name='eventos'

urlpatterns = [
    url('index', index, name='index'),
    url(regex=r"^create$", view=EventCreate.as_view(), name="create_event"),
    url(regex=r"^list$", view=EventList.as_view(), name="list_event"),
    url(r'^update/(?P<pk>\d+)/$', EventUpdate.as_view(), name='update_event'),
    url(r'^delete/(?P<pk>\d+)/$', EventDelete.as_view(), name='delete_event'),
    url(regex=r"^locations/(?P<id_evento>[\w-]+)$", view=EventLocationManage, name="locations"),
]