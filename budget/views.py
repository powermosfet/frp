# Create your views here.
from django.views.generic import *
from budget.models import *
from django.http import HttpResponseServerError
from django.core.urlresolvers import reverse
from datetime import date

class BudgetView(DetailView):
    model = Budget

    def get_object(self, queryset=None):
        if 'pk' not in self.kwargs.keys():
            obj = Budget.objects.order_by('-pk')[0]
        else:
            obj = super(BudgetView, self).get_object(queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super(BudgetView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('category')
        context['budgets'] = Budget.objects.all()
        return context

class AccountingView(ListView):
    model = Transaction
    year = date.today().year
    month = date.today().month

    def get(self, *args, **kwargs):
        if 'month' in kwargs.keys():
            self.month = kwargs['month']
        if 'year' in kwargs.keys():
            self.year = kwargs['year']
        return super(AccountingView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AccountingView, self).get_context_data(**kwargs)
        context['year'] = self.year
        context['month'] = self.month
        return context

class BudgetCreate(CreateView):
    model = Budget
    fields = ['description']

    def get_success_url(self):
        return reverse('budget_main')

class CategoryCreate(CreateView):
    model = Category
    fields = ['name', 'parent']

    def get_success_url(self):
        return reverse('budget_main')

class EntryCreate(CreateView):
    model = Entry
    fields = ['category', 'amount',
              'payments_per_year', 'budget']

    def form_valid(self, form):
        if form.instance.budget is not None:
            self.budget = form.instance.budget.pk
        return super(EntryCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('budget', kwargs={'pk': self.budget})
