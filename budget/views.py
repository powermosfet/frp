from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.views.generic.dates import MonthArchiveView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin, DeletionMixin
from django.forms import *
from budget.models import *
from django.http import *
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import *
import dateutil.parser
from calendar import monthrange as mr
from decimal import Decimal
from family.views import *

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

    def get_context_data(self, *args, **kwargs):
        context = super(BudgetView, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.filter(family = self.request.session['family']).order_by('string')
        context['budgets'] = Budget.objects.filter(family = self.request.session['family'])
        context['entries'] = self.get_object().entry_set.order_by('category__string')
        return context

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = [ 'family' ]

class AccountingView(ListView):
    template_name = 'budget/transaction_list.html'
    queryset = Transaction.objects.order_by('-date')[:10]

    def get_context_data(self, **kwargs):
        context = super(AccountingView, self).get_context_data(**kwargs)
        context['form'] = TransactionForm()
        context['form'].fields['category'].queryset = Category.objects.filter(family = self.request.session['family'])
        return context

class TransactionArchive(MonthView):
    model = Transaction

class TransactionDelete(DeleteView):
    model = Transaction
    template_name = 'budget/generic_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('accounting_main')

class TransactionUpdate(UpdateView):
    model = Transaction
    template_name = 'budget/generic_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('accounting',
                kwargs = { 'year': self.object.date.year, 'month': self.object.date.month})

class TransactionCreate(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/generic_form.html'

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit = False)
        family_id = int( self.request.session['family'] )
        self.object.family = Family.objects.get(pk = family_id)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        return reverse_lazy('accounting')

class BudgetForm(ModelForm):
    copy_from = ModelChoiceField(queryset = Budget.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        family_pk = kwargs.pop('family')
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.fields['copy_from'].queryset = Budget.objects.filter(family = family_pk)

    class Meta:
        model = Budget
        exclude = [ 'family' ]

class BudgetCreate(CreateView):
    template_name = 'budget/generic_form.html'
    form_class = BudgetForm

    def get_form_kwargs(self):
        return { 'family': self.request.session['family'] }

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit = False)
        family_id = int( self.request.session['family'] )
        self.object.family = Family.objects.get(pk = family_id)
        copy_from = form.cleaned_data['copy_from']
        if copy_from is not None:
            for e in copy_from.entry_set.all():
                e.pk = None
                e.budget = self.object
                e.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('budget_main')

class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(family = self.instance.family)

    class Meta:
        model = Category
        exclude = [ 'family' ]

class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'budget/generic_form.html'

    def get_form_kwargs(self):
        c = Category()
        c.family = Family.objects.get(pk = self.request.session['family'])
        return { 'instance': c }

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit = False)
        family_id = int( self.request.session['family'] )
        self.object.family = Family.objects.get(pk = family_id)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('budget_main')

class CategoryChange(UpdateView):
    model = Category
    template_name = 'budget/generic_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('budget_main')

class CategoryDelete(DeleteView):
    model = Category
    template_name = 'budget/generic_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('budget_main')

class EntryDelete(DeleteView):
    model = Entry
    template_name = 'budget/generic_form.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('budget_main')

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

    def get_success_url(self, **kwargs):
        return reverse('budget', kwargs={'pk': self.budget})

    def form_valid(self, form):
        if form.instance.budget is not None:
            self.budget = form.instance.budget.pk
        return super(EntryUpdate, self).form_valid(form)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

class CompareForm(Form):
    budget = ModelChoiceField(Budget.objects.order_by('-pk'))
    date_from = DateField()
    date_to = DateField()

class Comparison(object):
    def __init__(self, date_from, date_to, entry):
        self.budgeted_amount = Decimal()
        self.category = entry.category
        days = (date_to - date_from).days
        if days > 0:
            self.budgeted_amount = entry.amount() * entry.payments_per_year * Decimal(days / 365.0)
        self.actual_amount = sum(t.result()
                                    for t in Transaction.objects
                                        .filter(date__range=(date_from, date_to))
                                        if t.category.is_or_child(entry.category)
                                )

    def diff(self):
        return self.actual_amount - self.budgeted_amount 

class UnbudgetedComparison(Comparison):
    def __init__(self, date_from, date_to, budget):
        self.budgeted_amount = Decimal()
        self.category = None
        self.actual_amount = sum(t.result()
                                    for t in Transaction.objects
                                        .filter(date__range=(date_from, date_to))
                                        if all(not t.category.is_or_child(e.category)
                                            for e in budget.entry_set.all()
                                            )
                                )

class Compare(ListView):
    template_name = 'budget/compare.html'
    context_object_name = 'comparisons'

    def get(self, *args, **kwargs):
        t = date.today()
        y, m = t.year, t.month
        self.date_from_str = self.request.GET.get('date_from')
        self.date_to_str = self.request.GET.get('date_to')
        try:
            self.date_from = dateutil.parser.parse(self.date_from_str)
            self.date_to = dateutil.parser.parse(self.date_to_str)
        except:
            self.date_from_str = date(y, m, 1          ).isoformat()
            self.date_to_str   = date(y, m, mr(y, m)[1]).isoformat()
            self.date_from = dateutil.parser.parse(self.date_from_str)
            self.date_to = dateutil.parser.parse(self.date_to_str)
        self.budget_pk = self.request.GET.get('budget')
        self.budget = Budget.objects.filter(pk=self.budget_pk).first()
        if self.budget is None:
            self.budget = Budget.objects.last()
            self.budget_pk = self.budget.pk
        self.comparisons = [ Comparison(self.date_from, self.date_to, en )
                            for en in self.budget.entry_set.all() ]
        self.comparisons.append(UnbudgetedComparison(self.date_from, self.date_to, self.budget ))
        return super(Compare, self).get(*args, **kwargs)


    def get_queryset(self, *args, **kwargs):
        return self.comparisons

    def get_context_data(self, **kwargs):
        context = super(Compare, self).get_context_data(**kwargs)
        context['budget'] = self.budget
        context['form'] = CompareForm(initial = { 'budget':    self.budget_pk,
                                                  'date_from': self.date_from_str,
                                                  'date_to':   self.date_to_str,     
                                                })
        return context
