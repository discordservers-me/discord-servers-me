from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def meta_description():
    return settings.META_DESCRIPTION
