from django import template
register = template.Library()

@register.filter
def split(value, delimiter=' '):
    """Splits a string by the given delimiter (default is space)."""
    if value:
        return value.split(delimiter)
    return []

@register.filter
def index(seq, i):
    try:
        return seq[i]
    except:
        return ''

@register.filter
def make_list(value):
    return range(int(value))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, "")

@register.filter
def replace(value, arg):
    old, new = arg.split(',')
    return value.replace(old, new)

