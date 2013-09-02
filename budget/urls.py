from django.conf.urls import patterns, include, url
from budget.views import *

urlpatterns = patterns('',
    url(r'^$', BudgetView.as_view(), name='budget_main'),
    url(r'^accounting/$', AccountingView.as_view(), name='accounting_main'),
    url(r'^budget/(?P<pk>\d+)/$', BudgetView.as_view(), name='budget'),
    url(r'^budget/create/$', BudgetCreate.as_view(), name='budget_create'),
    url(r'^category/create/$', CategoryCreate.as_view(), name='category_create'),
    url(r'^entry/create/$', EntryCreate.as_view(), name='entry_create'),

)
