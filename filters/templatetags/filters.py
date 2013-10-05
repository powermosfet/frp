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
    return n.quantize(Decimal('0.01'))

@register.filter('month')
def month(m):
    if m == '': return 'No month'
    return m.strftime('%B %Y')
