from django.conf.urls import patterns, include, url
from budget.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$',                                         login_required(BudgetView.as_view()),                      name='budget_main'),
    url(r'^budget/(?P<pk>\d+)/$',                      login_required(BudgetView.as_view()),                      name='budget'),
    url(r'^budget/create/$',                           login_required(BudgetCreate.as_view()),                    name='budget_create'),
    url(r'^accounting/$',                              login_required(AccountingView.as_view()),                  name='accounting'),
    url(r'^accounting/create_transaction/$',           login_required(TransactionCreate.as_view()),               name='transaction_create'),
    url(r'^accounting/transaction/(?P<pk>\d+)/$',      login_required(TransactionUpdate.as_view()),               name='transaction_update'),
    url(r'^accounting/transaction/(?P<pk>\d+)/del/$',  login_required(TransactionDelete.as_view()),               name='transaction_delete'),
    url(r'^accounting/transaction/(?P<year>\d+)/(?P<month>\d+)/$',      login_required(TransactionArchive.as_view(month_format='%m')),               name='transaction_archive'),
    url(r'^category/create/$',                         login_required(CategoryCreate.as_view()),                  name='category_create'),
    url(r'^category/(?P<pk>\d+)/$',                    login_required(CategoryChange.as_view()),                  name='category_change'),
    url(r'^category/(?P<pk>\d+)/del/$',                login_required(CategoryDelete.as_view()),                  name='category_del'),
    url(r'^entry/create/$',                            login_required(EntryCreate.as_view()),                     name='entry_create'),
    url(r'^entry/(?P<pk>\d+)/$',                       login_required(EntryUpdate.as_view()),                     name='entry_update'),
    url(r'^entry/(?P<pk>\d+)/del/$',                   login_required(EntryDelete.as_view()),                     name='entry_del'),
    url(r'^compare/$',                                 login_required(Compare.as_view()),                         name='compare'),
)
