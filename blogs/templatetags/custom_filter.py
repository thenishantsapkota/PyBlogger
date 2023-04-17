from django import template

register = template.Library()


@register.filter
def format_datetime(value):
    return value.strftime("%I:%M %p")
