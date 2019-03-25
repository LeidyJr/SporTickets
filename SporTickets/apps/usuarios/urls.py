from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from .views import *

app_name='usuarios'

urlpatterns = [
    url('signup', signup, name='signup'),
]