from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from django.forms import *
from family.models import *

# Create your views here.

class LoginForm(AuthenticationForm):
    family = ModelChoiceField(queryset=Family.objects.all())

def family_login(request, *args, **kwargs):
    if request.method == 'POST':
        pk = request.POST.get('family', None)
        f = Family.objects.get(pk = pk)
        request.session['family'] = pk
        request.session['family_name'] = f.name
    return login(request, *args, **kwargs)
