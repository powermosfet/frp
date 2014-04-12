from django.conf.urls import patterns, include, url
from piston.resource import Resource
from api.authentication import *
from api.handlers import *

auth = HttpBasicAuthentication(realm="frp")
budget_resource = Resource(BudgetHandler, authentication=auth)

urlpatterns = patterns('',
           url(r'^budgets/(?P<id>\d+)$', budget_resource),
              url(r'^budgets$', budget_resource),
              )
