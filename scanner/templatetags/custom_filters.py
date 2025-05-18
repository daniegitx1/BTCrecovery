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
    except Exception:
        return ''

@register.filter
def make_list(value):
    return range(int(value))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, "")

@register.filter
def replace(value, arg):
    try:
        old, new = arg.split(',')
        return value.replace(old, new)
    except ValueError:
        return value  # Return original if input is malformed

@register.filter
def prettify_label(value):
    """Replaces underscores with spaces and capitalizes the result."""
    if isinstance(value, str):
        return value.replace('_', ' ').capitalize()
    return value

@register.filter
def not_in(value, arg):
    """Checks if value is not in a comma-separated string list."""
    excluded = [item.strip() for item in arg.split(",")]
    return value not in excluded
