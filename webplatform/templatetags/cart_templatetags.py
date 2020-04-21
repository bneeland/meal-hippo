from django import template
from .. import models

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        queryset = models.Order.objects.filter(user=user, is_completed=False)
        if queryset.exists():
            return queryset[0].items.count()
    return 0
