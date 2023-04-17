import bleach
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def md(value):
    html = markdown.markdown(value)
    clean_html = bleach.clean(
        html,
        tags=list(bleach.ALLOWED_TAGS) + ["br", "p"],
        attributes=bleach.ALLOWED_ATTRIBUTES,
    )

    return mark_safe(clean_html)
