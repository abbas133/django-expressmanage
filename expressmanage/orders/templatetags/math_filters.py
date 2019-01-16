from django import template


register = template.Library()


@register.filter(name='isub')
def subtract_value(value, num):
    return int(value) - int(num)