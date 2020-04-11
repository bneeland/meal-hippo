from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy

from . import models

class SupportView(TemplateView):
    template_name = 'webplatform/support_view.html'

class AboutView(TemplateView):
    template_name = 'webplatform/about_view.html'

class ContactView(TemplateView):
    template_name = 'webplatform/contact_view.html'

class HomeView(TemplateView):
    template_name = 'webplatform/home_view.html'
