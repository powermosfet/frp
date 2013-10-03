from django.views.generic import *
from django import forms
from budget.models import *
from django.http import *
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import *

class BudgetView(DetailView):
    model = Budget

    def get_object(self, queryset=None):
        if 'pk' not in self.kwargs.keys():
            if Budget.objects.count() > 0:
                obj = Budget.objects.order_by('-pk')[0]
            else:
                obj = Budget()
        else:
            obj = super(BudgetView, self).get_object(queryset)
        return obj

    def get_context_data(self, **kwargs):
        context = super(BudgetView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('string')
        context['budgets'] = Budget.objects.all()
        return context

class AccountingView(CreateView):
    template_name = 'budget/transaction_list.html'
    model = Transaction
    year = date.today().year
    month = date.today().month

    def get_context_data(self, **kwargs):
        context = super(AccountingView, self).get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.order_by('-date')
        context['calendar'] = self.build_calendar()
        return context

    def build_calendar(self):
        calendar = []
        week = [ 0 for x in range(7) ]
        one_day = timedelta(1)
        year = int(self.year)
        month = int(self.month)
        first_day = date(year, month, 1)
        last_day = first_day + timedelta(days = 31)
        last_day.replace(day = 1)
        for d in daterange(first_day, last_day):
            week[d.weekday()] = d.day
            if d.weekday() >= 6:
                calendar.append(week)
                week = [ 0 for x in range(7) ]
        if any([ x != 0 for x in week ]):
            calendar.append(week)
        return calendar

class BudgetCreate(CreateView):
    model = Budget
    success_url = reverse_lazy('budget_main')

class CategoryCreate(CreateView):
    model = Category
    success_url = reverse_lazy('budget_main')

class CategoryChange(UpdateView):
    model = Category
    success_url = reverse_lazy('budget_main')

class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('budget_main')

class EntryCreate(CreateView):
    model = Entry
    fields = ['category', 'amount_abs', 'factor'
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
