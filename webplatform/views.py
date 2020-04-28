from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages

import stripe
stripe.api_key = "sk_test_nHnTQsXHpYu7VG1Dvl9z7dNi00Wgb8xDNd"

from . import models

class SupportView(TemplateView):
    template_name = 'webplatform/support_view.html'

class ContactView(TemplateView):
    template_name = 'webplatform/contact_view.html'

class HomeView(TemplateView):
    template_name = 'webplatform/home_view.html'

class OrderItemsView(ListView):
    model = models.Supplier
    template_name = 'webplatform/order_items_view.html'
    context_object_name = 'active_suppliers'

    def get_queryset(self):
        return models.Supplier.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            order_qs = models.Order.objects.filter(user=self.request.user, is_completed=False)
            if order_qs.exists():
                order = order_qs[0]
                context['order'] = order
                order_items = order.items.all()
                context['order_items'] = order_items
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
            messages.info(request, "Dish added")
        else:
            order.items.add(order_item)
            messages.info(request, "Dish added")
    else:
        order = models.Order.objects.create(user=request.user, is_completed=False)
        order.items.add(order_item)
        messages.info(request, "Dish added")
    return redirect("webplatform:order_items_view")

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
                messages.info(request, "Dish removed")
            else:
                order_item.delete()
                # messages.info(request, "Dish removed")
        else:
            messages.info(request, "No dish to remove")
    else:
        messages.info(request, "No dish to remove")
    return redirect("webplatform:order_items_view")

class OrderTimingView(LoginRequiredMixin, UpdateView):
    login_url = 'login'

    model = models.Order
    fields = ['delivery_date', 'delivery_time']
    template_name = 'webplatform/order_timing_view.html'
    success_url = reverse_lazy('webplatform:order_delivery_view')

    def get_object(self):
        order_qs = models.Order.objects.filter(user=self.request.user, is_completed=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.count() > 0:
                return order

class OrderDeliveryView(LoginRequiredMixin, UpdateView):
    login_url = 'login'

    model = models.UserDeliveryDetail
    fields = ['phone', 'address', 'instructions',]
    template_name = 'webplatform/order_delivery_view.html'
    success_url = reverse_lazy('webplatform:order_payment_view')

    def get_object(self):
        return get_object_or_404(models.UserDeliveryDetail, user=self.request.user)

def index(request):
	return render(request, 'webplatform/order_payment_view.html')

def charge(request):
	amount = 5
	if request.method == 'POST':
		print('Data:', request.POST)

	return render(request, 'webplatform/order_payment_view.html')
