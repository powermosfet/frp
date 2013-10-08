from django.views.generic import *
from django.views.generic.dates import MonthArchiveView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin, DeletionMixin
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
        context['entries'] = self.get_object().entry_set.order_by('category__string')
        return context

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction

class AccountingView(MonthArchiveView):
    template_name = 'budget/transaction_list.html'
    queryset = Transaction.objects.order_by('date')
    date_field = 'date'
    allow_future = True
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super(AccountingView, self).get_context_data(**kwargs)
        context['calendar'] = self.build_calendar()
        context['form'] = TransactionForm()
        return context

    def build_calendar(self):
        calendar = []
        week = [ 0 for x in range(7) ]
        one_day = timedelta(1)
        first_day = date(int(self.get_year()), int(self.get_month()), 1)
        last_day = self.get_next_month(first_day)
        for d in daterange(first_day, last_day):
            week[d.weekday()] = d.day
            if d.weekday() >= 6:
                calendar.append(week)
                week = [ 0 for x in range(7) ]
        if any([ x != 0 for x in week ]):
            calendar.append(week)
        return calendar
    
class TransactionSuggestion(object):
    def __init__(self, category, comment, amount, date):
        self.category = category
        self.comment = comment
        self.amount = amount
        self.date = date

def AccountingDefaultView(req):
    return HttpResponseRedirect(reverse_lazy('accounting', args = ( date.today().year, date.today().month )))

class TransactionDelete(DeleteView):
    model = Transaction
    success_url = reverse_lazy('accounting_main')
    template_name = 'budget/generic_form.html'

class TransactionUpdate(UpdateView):
    model = Transaction
    success_url = reverse_lazy('accounting_main')
    template_name = 'budget/generic_form.html'

class TransactionCreate(CreateView):
    model = Transaction
    template_name = 'budget/generic_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('accounting', 
                kwargs = { 'year': self.object.date.year, 'month': self.object.date.month})

class BudgetCreate(CreateView):
    model = Budget
    success_url = reverse_lazy('budget_main')
    template_name = 'budget/generic_form.html'

class CategoryCreate(CreateView):
    model = Category
    success_url = reverse_lazy('budget_main')
    template_name = 'budget/generic_form.html'

class CategoryChange(UpdateView):
    model = Category
    success_url = reverse_lazy('budget_main')
    template_name = 'budget/generic_form.html'

class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('budget_main')
    template_name = 'budget/generic_form.html'

class EntryDelete(DeleteView):
    model = Entry
    success_url = reverse_lazy('budget_main')
    template_name = 'budget/generic_form.html'

class EntryCreate(CreateView):
    model = Entry
    template_name = 'budget/generic_form.html'

    def get_success_url(self, **kwargs):
        return reverse('budget', kwargs={'pk': self.budget})

    def form_valid(self, form):
        if form.instance.budget is not None:
            self.budget = form.instance.budget.pk
        return super(EntryCreate, self).form_valid(form)

class EntryUpdate(UpdateView, DeletionMixin):
    model = Entry
    template_name = 'budget/generic_form.html'

    def delete(self, r, *args, **kwargs):
        import pdb;pdb.set_trace()
        return super(EntryUpdate, self).delete(r, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse('budget', kwargs={'pk': self.budget})

    def form_valid(self, form):
        if form.instance.budget is not None:
            self.budget = form.instance.budget.pk
        return super(EntryUpdate, self).form_valid(form)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def compareView(r):
    return HttpResponseRedirect(
            reverse_lazy('compare', kwargs={ 'pk': Budget.objects.order_by('-pk')[0].pk,
                                             'year'  : date.today().year,
                                             'month' : date.today().month }))

class Compare(SingleObjectMixin, MonthArchiveView):
    queryset = Transaction.objects.order_by('date')
    template_name = 'budget/compare.html'
    date_field = 'date'
    allow_future = True
    allow_empty = True

    def get(self, *args, **kwargs):
        self.object = self.get_object(Budget.objects.all())
        return super(Compare, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Compare, self).get_context_data(**kwargs)
        context['object'] = self.object
        return context

    def get_object(self, queryset = None):
        return super(Compare, self).get_object(queryset)
