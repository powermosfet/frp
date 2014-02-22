from django.shortcuts import render
from django.views.generic import *

# Create your views here.

class FamilyMixin(View):

    def get(self, *args, **kwargs):
        self.family = kwargs['family']
        return super(FamilyMixin, self).get(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(FamilyMixin, self).get_context_data(*args, **kwargs)
        context['family'] = self.family
        return context
