from django import template
from django.contrib.auth.forms import AuthenticationForm

register = template.Library()

@register.simple_tag(takes_context=True)
def get_login_form(context):
    form = context.get('form', None)
    if form and isinstance(form, AuthenticationForm):
        return form
    return AuthenticationForm()