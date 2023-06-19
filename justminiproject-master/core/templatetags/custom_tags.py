from django import template

register = template.Library()

@register.filter
def break_loop(value, num):
    return value[:num]
