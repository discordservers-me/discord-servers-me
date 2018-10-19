from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def meta_title():
    return settings.META_TITLE
