from django import template
from decimal import Decimal

register = template.Library()

@register.filter('two_decimals')
def two_decimals(inp):
    return inp.quantize(Decimal('0.01'))
