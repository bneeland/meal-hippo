from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, ListView
from django.urls import reverse, reverse_lazy

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
