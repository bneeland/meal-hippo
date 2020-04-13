from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, ListView
from django.urls import reverse
from django.utils import timezone

from . import models

class SupportView(TemplateView):
    template_name = 'webplatform/support_view.html'

class ContactView(TemplateView):
    template_name = 'webplatform/contact_view.html'

class HomeView(TemplateView):
    template_name = 'webplatform/home_view.html'

class DishesView(ListView):
    queryset = models.Supplier.objects.filter(is_active=True)
    context_object_name = 'suppliers'
    template_name = 'webplatform/dishes_view.html'

def add_to_cart(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    order_item, created = models.OrderItem.objects.get_or_create(item=item, user=request.user, is_completed=False)
    order_qs = models.Order.objects.filter(user=request.user, is_completed=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = models.Order.objects.create(user=request.user, delivery_at=timezone.now(), is_completed=False)
        order.items.add(order_item)
    return redirect("webplatform:dishes_view")
