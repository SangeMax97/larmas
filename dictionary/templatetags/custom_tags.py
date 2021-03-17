from django import template

register = template.Library()

counter = 0

@register.filter
def increment(v1, v2):
    v1 = v1 +1
    v2 = v2 +1
    v = v1 + v2
    return v
