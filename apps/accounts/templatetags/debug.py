from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
def as_dict(value):
    return value.__dict__


@register.filter
def stringify(value):
    return str(value)


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def log(val: str):
    print(val)


@register.filter
@stringfilter
def split(string: str, sep):
    return string.split(sep)


@register.filter
def index(sequence, i):
    return sequence[i]
