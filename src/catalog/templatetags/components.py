import uuid

from django import template
from django import forms
from django.urls import reverse_lazy

register = template.Library()


@register.inclusion_tag('catalog/components/input_text_field.html')
def input_text_field(field):
    return {
        'field': field
    }


@register.inclusion_tag('catalog/components/button.html')
def button(label, raised=True, href="", submit=False, url=""):
    link = href

    if not href and url:
        link = reverse_lazy(url)

    return {
        'label': label,
        'raised': raised,
        'href': link,
        'submit': submit
    }
