from django import template
from decimal import Decimal

register = template.Library()

@register.filter('two_decimals')
def two_decimals(inp):
    return inp.quantize(Decimal('0.01'))

@register.filter('month')
def month(m):
    if m == '': return 'No month'
    ms = [ 'january',
            'february',
            'march',
            'april',
            'may',
            'june',
            'july',
            'august',
            'september',
            'october',
            'november',
            'december' ]
    return ms[int(m) - 1]
