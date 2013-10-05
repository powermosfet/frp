from django.conf.urls import patterns, include, url
from budget.views import *

urlpatterns = patterns('',
    url(r'^$', BudgetView.as_view(), name='budget_main'),
    url(r'^budget/(?P<pk>\d+)/$', BudgetView.as_view(), name='budget'),
    url(r'^budget/create/$', BudgetCreate.as_view(), name='budget_create'),
    url(r'^accounting/$', AccountingDefaultView, name='accounting_main'),
    url(r'^accounting/(?P<year>\d+)/(?P<month>\d+)/$', AccountingView.as_view(month_format='%m'), name='accounting'),
    url(r'^accounting/create_transaction/$', TransactionCreate.as_view(), name='transaction_create'),
    url(r'^accounting/transaction/(?P<pk>\d+)/$', TransactionUpdate.as_view(), name='transaction_update'),
    url(r'^accounting/transaction/(?P<pk>\d+)/del/$', TransactionDelete.as_view(), name='transaction_delete'),
    url(r'^category/create/$', CategoryCreate.as_view(), name='category_create'),
    url(r'^category/change/(?P<pk>\d+)/$', CategoryChange.as_view(), name='category_change'),
    url(r'^category/del/(?P<pk>\d+)/$', CategoryDelete.as_view(), name='category_del'),
    url(r'^entry/create/$', EntryCreate.as_view(), name='entry_create'),

)
