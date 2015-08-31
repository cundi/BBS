from django import template
from django.core.paginator import Paginator
register = template.Library()

@register.filter(name='paginator')
def paginator(request,queryset, pages=None):
    p_qy = Paginator(queryset, pages)

