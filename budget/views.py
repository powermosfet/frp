# Create your views here.
from django.views.generic import *
from budget.models import *
from django.http import HttpResponseServerError
from django.core.urlresolvers import reverse
from datetime import *

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
        context['calendar'] = self.build_calendar()
        context['categories'] = Category.objects.order_by('category')
        return context

    def build_calendar(self):
        calendar = []
        week = [ 0 for x in range(7) ]
        one_day = timedelta(1)
        year = int(self.year)
        month = int(self.month)
        for d in daterange(date(year, month, 1), date(year, month + 1, 1)):
            week[d.weekday()] = d.day
            if d.weekday() >= 6:
                calendar.append(week)
                week = [ 0 for x in range(7) ]
        if any([ x != 0 for x in week ]):
            calendar.append(week)
        return calendar

class TransactionCreate(CreateView):
    model = Transaction
    fields = ['date', 'category', 'amount', 'comment']
    template = 'budget/transaction_list.html'

    def get_success_url(self):
        return reverse('accounting', year, month)

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

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
