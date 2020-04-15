from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, ListView
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from . import models

class SupportView(TemplateView):
    template_name = 'webplatform/support_view.html'

class ContactView(TemplateView):
    template_name = 'webplatform/contact_view.html'

class HomeView(TemplateView):
    template_name = 'webplatform/home_view.html'

class DishesView(ListView):
    queryset = models.Supplier.objects.filter(is_active=True)
    context_object_name = 'active_suppliers'
    template_name = 'webplatform/dishes_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_qs = models.Order.objects.filter(user=self.request.user, is_completed=False)
        if order_qs.exists():
            order = order_qs[0]
            order_items = order.items.all()
            context['order_items'] = order_items
            print(context)
            return context

def add_to_order(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    order_item, created = models.OrderItem.objects.get_or_create(item=item, user=request.user, is_completed=False)
    order_qs = models.Order.objects.filter(user=request.user, is_completed=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The dish quantity in your order was increased successfully.")
        else:
            order.items.add(order_item)
            messages.info(request, "The dish was added successfully to your order.")
    else:
        order = models.Order.objects.create(user=request.user, delivery_at=timezone.now(), is_completed=False)
        order.items.add(order_item)
        messages.info(request, "The dish was added successfully to your order.")
    return redirect("webplatform:dishes_view")

def remove_from_order(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    order_qs = models.Order.objects.filter(user=request.user, is_completed=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item_qs = models.OrderItem.objects.filter(item=item, user=request.user, is_completed=False)
            order_item = order_item_qs[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "The dish quantity in your order was decreased successfully.")
            else:
                order_item.delete()
                messages.info(request, "The dish was removed successfully from your order.")
        else:
            messages.info(request, "The dish was not in your order.")
    else:
        messages.info(request, "There is nothing in your order at the moment.")
    return redirect("webplatform:dishes_view")
