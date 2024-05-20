from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Splits a string into a list using the key as the delimiter.
    """
    return value.split(key)


@register.filter(name='remove_brackets')
def remove_brackets(value):
    if isinstance(value, str):
        elements = value.strip('[]').replace("'", "").split(', ')
        return ", ".join(elements)
    else:
        return value



