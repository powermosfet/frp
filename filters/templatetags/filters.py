from django import template
from decimal import Decimal

register = template.Library()

@register.filter('type')
def type_of(inp):
    return str(type(inp))

@register.filter('two_decimals')
def two_decimals(inp):
    if type(inp) is not Decimal:
        n = Decimal()
    else:
        n = inp
    return "{0:.2f}".format(inp)

@register.filter('month')
def month(m):
    if m == '': return 'No month'
    return m.strftime('%B %Y')

@register.filter('amount_css_class')
def amount_css_class(amount):
    if amount < 0: return 'negative'
    else: return ''

@register.filter('in_category')
def in_category(transactions, category):
    return [ t for t in transactions if t.category.is_or_child(category) ]

@register.filter('tr_sum')
def tr_sum(transactions):
    return sum(t.result() for t in transactions)

@register.filter('subtract')
def subtract(a, b):
    return Decimal(float(a) - float(b))

@register.filter('status_css_class')
def subtract(diff, budgeted):
    if diff < 0:
        if abs(diff) / budgeted < 0.1: return 'status_ok'
        else:                          return 'status_bad'
    else:                              return 'status_good'

