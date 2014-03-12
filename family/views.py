from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import *
from django.contrib.auth.views import login
from django.contrib.auth.forms import UserCreationForm
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

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'password', 'email' ]

class Register(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'family/register.html'

class Profile(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'family/profile.html'

class FamilyCreateBase(CreateView):
    def get_form(self, form, *args, **kwargs):
        f = super(FamilyCreateBase, self).get_form(form, *args, **kwargs)
        f.fields.pop('family')
        return f

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        fam_pk = self.request.session['family']
        self.object.family = Family.objects.get(pk = fam_pk)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
