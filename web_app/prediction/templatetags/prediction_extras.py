from django import template

register = template.Library()

@register.filter
def replace(value, args):
    """
    Replaces characters in a string.
    Usage: {{ value|replace:"old,new" }}
    """
    if args and ',' in args:
        old, new = args.split(',', 1)
        return value.replace(old, new)
    return value

@register.filter
def replace_underscore(value):
    """
    Replaces underscores with spaces.
    Usage: {{ value|replace_underscore }}
    """
    if isinstance(value, str):
        return value.replace('_', ' ')
    return value
