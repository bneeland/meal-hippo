from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_API_SECRET_KEY

from . import models
from . import forms
from . import tasks

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
            order_item.quantity += item.portion_increment
            order_item.save()
            messages.info(request, "Portion added")
        else:
            order.items.add(order_item)
            order_item.quantity += (item.minimum_portions - 1)
            order_item.save()
            messages.info(request, "Dish added")
    else:
        order = models.Order.objects.create(user=request.user, is_completed=False)
        order.items.add(order_item)
        order_item.quantity += (item.minimum_portions - 1)
        order_item.save()
        messages.info(request, "Dish added")

        tasks.send_mail_with_celery.delay(
            subject='New order created on mealhippo.com',
            message='A new order was created on mealhippo.com. The user who did this was '+request.user.email+'. This was done at '+str(timezone.localtime(timezone.now()))+'.'
        )

    return redirect("webplatform:order_items_view")

def remove_from_order(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    order_qs = models.Order.objects.filter(user=request.user, is_completed=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item_qs = models.OrderItem.objects.filter(item=item, user=request.user, is_completed=False)
            order_item = order_item_qs[0]
            if order_item.quantity > item.minimum_portions:
                order_item.quantity -= item.portion_increment
                order_item.save()
                messages.info(request, "Portion removed")
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

    template_name = 'webplatform/order_timing_view.html'
    form_class = forms.OrderTimingForm
    success_url = reverse_lazy('webplatform:order_delivery_view')

    def get_object(self):
        order_qs = models.Order.objects.filter(user=self.request.user, is_completed=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.count() > 0:
                return order

class OrderDeliveryView(LoginRequiredMixin, UpdateView):
    login_url = 'login'

    template_name = 'webplatform/order_delivery_view.html'
    form_class = forms.OrderDeliveryForm
    success_url = reverse_lazy('webplatform:order_payment_view')

    def get_object(self):
        return get_object_or_404(models.UserDeliveryDetail, user=self.request.user)

class OrderPaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = models.Order.objects.get(user=self.request.user, is_completed=False)
        order_items = order.items.all()
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(self.request, 'webplatform/order_payment_view.html', context)

    def post(self, *args, **kwargs):
        user = self.request.user
        order = models.Order.objects.get(user=user, is_completed=False)
        token = self.request.POST.get('stripeToken')
        price = order.get_total_order_price()
        price_cents = int(price * 100)

        try:
            charge = stripe.Charge.create(
                amount=price_cents,
                currency='cad',
                source=token,
            )

            payment = models.Payment()
            payment.stripe_charge_id = charge["id"]
            payment.user = user
            payment.price = price
            payment.save()

            order.is_completed = True
            order.payment = payment
            order.save()

            # send_mail(
            #     subject='Order completed on mealhippo.com',
            #     message='An order was completed on mealhippo.com. The user\' email is '+user.email+'.',
            #     from_email='web.bot@mealhippo.com',
            #     recipient_list=['hello@mealhippo.com'],
            #     fail_silently=True,
            # )

            return redirect(reverse_lazy('webplatform:order_complete_view'))

        except stripe.error.CardError as e:
            error_message = e.error.message
            messages.error(self.request, f"{error_message}")
            return redirect(reverse_lazy('webplatform:order_payment_view'))
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit error")
            return redirect(reverse_lazy('webplatform:order_payment_view'))
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters")
            return redirect(reverse_lazy('webplatform:order_payment_view'))
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Payment keys incorrect--not authenticated")
            return redirect(reverse_lazy('webplatform:order_payment_view'))
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network error")
            return redirect(reverse_lazy('webplatform:order_payment_view'))
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect(reverse_lazy('webplatform:order_payment_view'))
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request, "An error unrelated to payment processing occurred")
            return redirect(reverse_lazy('webplatform:order_payment_view'))



class OrderCompleteView(TemplateView):
    template_name = 'webplatform/order_complete_view.html'
