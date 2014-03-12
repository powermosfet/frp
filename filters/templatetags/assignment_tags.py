from django import template
from decimal import Decimal
import datetime as dt

register = template.Library()

@register.assignment_tag
def current_year():
    return dt.date.today().year

@register.assignment_tag
def current_month():
    return dt.date.today().month

