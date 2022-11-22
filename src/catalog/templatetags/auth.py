import sys

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_perm(context, *args, **kwargs):
    auth = context['auth']
    return auth.check(args[0])
