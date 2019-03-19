from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def home(request):
	return render(request, 'usuarios/home.html')

def signup(request):
	form = UserCreationForm
	return render(request, 'usuarios/signup.html', {
		'form': form
		})
